#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

utils::golang::install() {
	# install golang
	curl -sL https://storage.googleapis.com/golang/go1.7.5.linux-amd64.tar.gz | tar -C /usr/local -zxf -
	echo 'PATH="/usr/local/sbin:/usr/local/bin:/usr/local/go/bin/:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/go/bin"' >> /etc/environment
	echo 'GOPATH="/go"' >> /etc/environment
}

utils::hyperd::install() {
    # install from https://docs.hypercontainer.io/get_started/install/linux.html
    apt-get update && apt-get install -y qemu libvirt-bin
    curl -sSL https://hypercontainer.io/install | bash
    echo -e "Hypervisor=libvirt\n\
Kernel=/var/lib/hyper/kernel\n\
Initrd=/var/lib/hyper/hyper-initrd.img\n\
Hypervisor=qemu\n\
StorageDriver=overlay\n\
gRPCHost=127.0.0.1:22318" > /etc/hyper/config
    curl https://hypercontainer-install.s3.amazonaws.com/hypercontainer_0.8.0-1_amd64.deb -o hypercontainer.deb
    curl https://hypercontainer-install.s3.amazonaws.com/hyperstart_0.8.0-1_amd64.deb -o hyperstart.deb
    dpkg -i hyperstart.deb hypercontainer.deb
    rm -f hyperstart.deb hypercontainer.deb
    systemctl enable hyperd
    systemctl restart hyperd
}

utils::docker::install() {
    apt-get install -y docker.io
    systemctl enable docker
    systemctl start docker
}

utils::frakti::install() {
    curl -sSL https://github.com/kubernetes/frakti/releases/download/v0.1/frakti -o /usr/bin/frakti
    chmod +x /usr/bin/frakti
    cat <<EOF > /lib/systemd/system/frakti.service
[Unit]
Description=Hypervisor-based container runtime for Kubernetes
Documentation=https://github.com/kubernetes/frakti
After=network.target
[Service]
ExecStart=/usr/bin/frakti --v=3 \
          --log-dir=/var/log/frakti \
          --logtostderr=false \
          --listen=/var/run/frakti.sock \
          --streaming-server-addr=%H \
          --hyper-endpoint=127.0.0.1:22318
MountFlags=shared
TasksMax=8192
LimitNOFILE=1048576
LimitNPROC=1048576
LimitCORE=infinity
TimeoutStartSec=0
Restart=on-abnormal
[Install]
WantedBy=multi-user.target
EOF

    systemctl enable frakti
    systemctl start frakti
}

utils::frakti::install-src() {
    if [[ -z "$(which go)" ]]; then
        echo "Can't find 'go' in PATH, please install golang first"
        exit 2
    fi
    export GOPATH=/go
    mkdir -p $GOPATH/src/k8s.io
    git clone https://github.com/kubernetes/frakti.git $GOPATH/src/k8s.io/frakti
    cd $GOPATH/src/k8s.io/frakti
    apt install build-essential -y && make && make install
    cat <<EOF > /lib/systemd/system/frakti.service
[Unit]
Description=Hypervisor-based container runtime for Kubernetes
Documentation=https://github.com/kubernetes/frakti
After=network.target
[Service]
ExecStart=/usr/bin/frakti --v=3 \
          --log-dir=/var/log/frakti \
          --logtostderr=false \
          --listen=/var/run/frakti.sock \
          --streaming-server-addr=%H \
          --hyper-endpoint=127.0.0.1:22318
MountFlags=shared
TasksMax=8192
LimitNOFILE=1048576
LimitNPROC=1048576
LimitCORE=infinity
TimeoutStartSec=0
Restart=on-abnormal
[Install]
WantedBy=multi-user.target
EOF

    systemctl enable frakti
    systemctl start frakti
}

utils::cni::install() {
    apt-get update && apt-get install -y apt-transport-https
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial-unstable main
EOF
    apt-get update
    apt-get install -y kubernetes-cni
    mkdir -p /etc/cni/net.d
    cat >/etc/cni/net.d/10-mynet.conf <<-EOF
{
    "cniVersion": "0.3.0",
    "name": "mynet",
    "type": "bridge",
    "bridge": "cni0",
    "isGateway": true,
    "ipMasq": true,
    "ipam": {
        "type": "host-local",
        "subnet": "10.244.1.0/24",
        "routes": [
            { "dst": "0.0.0.0/0"  }
        ]
    }
}
EOF
    cat >/etc/cni/net.d/99-loopback.conf <<-EOF
{
    "cniVersion": "0.3.0",
    "type": "loopback"
}
EOF
}

utils::kubelet::install() {
    apt-get update && apt-get install -y apt-transport-https
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial-unstable main
EOF
    apt-get update
    apt-get install -y kubelet kubeadm kubectl
    # Configure kubelet with frakti runtime
    sed -i '2 i\Environment="KUBELET_EXTRA_ARGS=--container-runtime=remote --container-runtime-endpoint=/var/run/frakti.sock --feature-gates=AllAlpha=true"' /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
    systemctl daemon-reload
}

utils::master::install() {
    kubeadm init --pod-network-cidr 10.244.0.0/16 --kubernetes-version latest
    # Optional: enable schedule pods on the master
    export KUBECONFIG=/etc/kubernetes/admin.conf
    kubectl taint nodes --all node-role.kubernetes.io/master:NoSchedule-
}

utils::node::install() {
    # get token on master node
    token="$1"
    master_ip="$2"
    # join master on worker nodes
    kubeadm join --token $token ${master_ip}
}

utils::kubectl::create-pod() {
    # create a pod with memory limits.
    kubectl create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
    resources:
      limits:
        memory: 128Mi
        cpu: 1000m
EOF
}

utils::kubectl::expose-pod() {
    pod=${POD:-"nginx"}
    kubectl expose "$pod" nginx --port=80
}

utils::kubectl::evaluate-dns() {
    pod=${POD:-"nginx"}
    kubectl exec -i -t $pod -- dig kubernetes.default.svc.cluster.local
}

utils::fix::dns-setup() {
    cat > /etc/resolv.conf <<EOF
search default.svc.cluster.local svc.cluster.local cluster.local home
nameserver 10.96.0.10
options ndots:5
EOF
}
