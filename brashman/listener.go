// Source - https://stackoverflow.com/questions/50032630/raw-socket-udp-programming
// Posted by Brash Man, modified by community. See post 'Timeline' for change history
// Retrieved 2025-12-15, License - CC BY-SA 4.0

package main
    
import (
    "syscall"
    "os"
    "fmt"
)

func main() {
    fd, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_RAW, syscall.IPPROTO_UDP)
    if err != nil {
        fmt.Println(err)
        return
    }
    sa:= &syscall.SockaddrInet4{
        Addr: [4]byte{127,0,0,1},
        Port:27288,
    }
    e := syscall.Bind(fd, sa)
    if e != nil {
        fmt.Println("problems @ location 1")
    }
    f := os.NewFile(uintptr(fd), fmt.Sprintf("fd%d", fd))
    fmt.Println("Entering main loop")
    for {
        fmt.Println("In loop")
        buf := make([]byte, 1024)
        numRead, err := f.Read(buf)
        if err != nil {
            fmt.Println("problems @ location 2")
        }
        fmt.Printf("Loop done %v\n", buf[:numRead])
    }

}

