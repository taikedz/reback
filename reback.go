package main

import (
    "fmt"
    "os"

    "github.com/taikedz/goargs/goargs"
)

func main() {
    var command string
    command_args, err := goargs.Unpack(os.Args[1:], &command)
    if err != nil {
        fmt.Printf("Error parsing args: %v\n", err)
        os.Exit(1)
    }

    parser := goargs.NewParser("reback : Report Back to peers")
    parser.RequireFlagDefs(true) // is not working?

    var broadcast_ip string = "127.0.0.255"
    var port uint

    if command == "start" {
        parser.UintVar(&port, "port", 43234, "Listening port")
    } else if command == "query" {
    } else {
        fmt.Printf("Unknown action : %s\n", command)
        os.Exit(1)
    }
    parser.Parse(command_args)

    remains, err := parser.UnpackArgs(0, &broadcast_ip)
    if err != nil {
        fmt.Printf("%v\n", err)
        os.Exit(1)
    }
    if len(remains) > 0 {
        fmt.Printf("Excess positional arguments: %v\n", remains)
        os.Exit(1)
    }

    fmt.Printf("Listening on port %d . Broadcasting to %s\nUnused: %v\n", port, broadcast_ip, remains)
}
