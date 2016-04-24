---
title: Tips for cgo
date: 2016-04-24 08:29:02
tags: [go]
---

cgo的一些tips

## 基本类型

The standard C numeric types are available under the names C.char, C.schar (signed char), C.uchar (unsigned char), C.short, C.ushort (unsigned short), C.int, C.uint (unsigned int), C.long, C.ulong (unsigned long), C.longlong (long long), C.ulonglong (unsigned long long), C.float, C.double, C.complexfloat (complex float), and C.complexdouble (complex double). The C type void* is represented by Go's unsafe.Pointer. The C types `__int128_t` and `__uint128_t` are represented by [16]byte.

To access a struct, union, or enum type directly, prefix it with struct_, union_, or enum_, as in C.struct_stat.

The size of any C type T is available as C.sizeof_T, as in C.sizeof_struct_stat.

As Go doesn't have support for C's union type in the general case, C's union types are represented as a Go byte array with the same length.

Go structs cannot embed fields with C types.

Any C function (even void functions) may be called in a multiple assignment context to retrieve both the return value (if any) and the C errno variable as an error (use _ to skip the result value if the function returns void). For example:

```
n, err := C.sqrt(-1)
_, err := C.voidFunc()
```

## 字符串类型转换

`C.CString`和`C.GoString`都会对原始数据做拷贝，不要忘记释放CString创建的内存：

```go
// Go string to C string
// The C string is allocated in the C heap using malloc.
// It is the caller's responsibility to arrange for it to be
// freed, such as by calling C.free (be sure to include stdlib.h
// if C.free is needed).
func C.CString(string) *C.char

// C string to Go string
func C.GoString(*C.char) string

// C data with explicit length to Go string
func C.GoStringN(*C.char, C.int) string

// C data with explicit length to Go []byte
func C.GoBytes(unsafe.Pointer, C.int) []byte
```

`C.CString`使用示例：

```go
ch := C.CString(str)
defer C.free(unsafe.Pointer(ch))
....
```

## 数组的使用

Go切片转为C数组：

```go
/*
#include <stdio.h>
void foo(double *arr, int len) {
	for(int i=0;i<len;i++) {
		printf("%f\n", arr[i]);
	}
}
*/
import "C"

func main() {
	arr := []float64{1, 2, 3, 4, 5}
	carr := (*C.double)(unsafe.Pointer(&arr[0]))
	C.foo(carr, C.int(len(arr)))

}
```

C数组转为Go切片

```go
import "unsafe"
import "fmt"

/*
#include <stdio.h>
#include <stdlib.h>
double* get_array(int n) {
	double *arr;
	arr = (double*)malloc(n*sizeof(arr));
	for(int i=0;i<n;i++)
	{
		arr[i]=i;
	}
	return arr;
}
*/
import "C"

func main() {
	size := 10
	carr := C.get_array(C.int(size))
	defer C.free(unsafe.Pointer(carr))
	arr := (*[1 << 30]float64)(unsafe.Pointer(carr))[:size:size]
	fmt.Println(arr)
}
```

C指针操作

```go
size := 10
carr := C.get_array(C.int(size))
defer C.free(unsafe.Pointer(carr))

// To go slice
arr := (*[1 << 30]float64)(unsafe.Pointer(carr))[:size:size]
for index := 0; index < size; index++ {
    // get value by C pointer operation
    value := *(*C.double)(unsafe.Pointer(uintptr(unsafe.Pointer(carr)) + uintptr(index)*unsafe.Sizeof(carr)))
    // get value by Go slice index
    gvalue := arr[index]
    fmt.Println(value, " == ", gvalue)
}
```

更多文档见https://golang.org/cmd/cgo/
