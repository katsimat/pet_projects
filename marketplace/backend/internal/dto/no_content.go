package dto

type NoContentResponse struct{}

func (NoContentResponse) StatusCode() int {
	return 204
}
