FROM golang:1.14

RUN go get -u github.com/golang/protobuf/protoc-gen-go && go get -u golang.org/x/tools/cmd/stringer &&     go get -u github.com/alvaroloes/enumer &&     go get golang.org/x/tools/cmd/goimports
