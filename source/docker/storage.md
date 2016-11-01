
# Storage

Storage driver | Commonly used on | Disabled on                                         
-------------- | ---------------- | ----------------------------------------------------
`overlay`      | `ext4` `xfs`     | `btrfs` `aufs` `overlay` `overlay2` `zfs` `eCryptfs`
`overlay2`     | `ext4` `xfs`     | `btrfs` `aufs` `overlay` `overlay2` `zfs` `eCryptfs`
`aufs`         | `ext4` `xfs`     | `btrfs` `aufs` `eCryptfs`                           
`btrfs`        | `btrfs` _only_   | N/A                                                 
`devicemapper` | `direct-lvm`     | N/A                                                 
`vfs`          | debugging only   | N/A                                                 
`zfs`          | `zfs` _only_     | N/A                                                 

![](https://docs.docker.com/engine/userguide/storagedriver/images/driver-pros-cons.png)
