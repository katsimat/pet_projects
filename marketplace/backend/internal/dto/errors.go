package dto

import "fmt"

type Response interface {
	StatusCode() int
}

type BadRequestError struct {
	Response Response
	Message  string
}

func (e *BadRequestError) Error() string {
	if e.Message != "" {
		return e.Message
	}
	return fmt.Sprintf("bad request: %d", e.Response.StatusCode())
}
