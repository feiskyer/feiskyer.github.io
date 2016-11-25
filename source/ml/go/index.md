# Tensorflow in Go

```
docker run -it feisky/tensorflow-go bash
```

```go
package main

import (
	"log"

	tf "github.com/tensorflow/tensorflow/tensorflow/go"
	"github.com/tensorflow/tensorflow/tensorflow/go/op"
)

func main() {
	s := op.NewScope()
	inp := op.Placeholder(s, tf.Double)
	out := op.Neg(s, inp)
	graph, err := s.Finalize()
	if err != nil {
		log.Fatal(err)
	}

	session, err := tf.NewSession(graph, nil)
	if err != nil {
		log.Fatal(err)
	}
	defer session.Close()

	inputData := []float64{-1, -2, 3}
	input, err := tf.NewTensor(inputData)
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("Input: %#v\n", inputData)
	output, err := session.Run(
		map[tf.Output]*tf.Tensor{
			inp: input,
		},
		[]tf.Output{out},
		[]*tf.Operation{out.Op})
	if err != nil {
		log.Fatal(err)
	}
	if len(output) != 1 {
		log.Fatalf("got %d outputs, want 1", len(output))
	}

	val := output[0].Value()
	log.Printf("Neg output %#v\n", val)
}

/* Output:
2016/11/22 14:37:54 Input: []float64{-1, -2, 3}
2016/11/22 14:37:54 Neg output []float64{1, 2, -3}
*/
```

View more documentation at <https://godoc.org/github.com/tensorflow/tensorflow/tensorflow/go>.

