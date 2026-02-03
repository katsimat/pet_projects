package main

import (
	"bytes"
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"os"
	"regexp"
	"strings"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s <types.go>\n", os.Args[0])
		os.Exit(1)
	}

	filename := os.Args[1]
	src, err := os.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
		os.Exit(1)
	}

	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, filename, src, parser.ParseComments)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing file: %v\n", err)
		os.Exit(1)
	}

	var methodsToAdd []string
	responsePattern := regexp.MustCompile(`Response(\d{3})$`)

	// Find all response types and add StatusCode methods
	ast.Inspect(f, func(n ast.Node) bool {
		switch x := n.(type) {
		case *ast.TypeSpec:
			typeName := x.Name.Name
			if strings.Contains(typeName, "Response") {
				// Try to extract status code from name like PingResponse200
				matches := responsePattern.FindStringSubmatch(typeName)
				if len(matches) == 2 {
					var statusCode int
					fmt.Sscanf(matches[1], "%d", &statusCode)
					if statusCode > 0 {
						method := fmt.Sprintf("\nfunc (r %s) StatusCode() int {\n\treturn %d\n}\n", typeName, statusCode)
						methodsToAdd = append(methodsToAdd, method)
					}
				}
			}
		}
		return true
	})

	if len(methodsToAdd) == 0 {
		return
	}

	// Append methods to the end of file
	var buf bytes.Buffer
	buf.Write(src)

	// Remove trailing whitespace
	content := bytes.TrimSpace(buf.Bytes())
	buf.Reset()
	buf.Write(content)
	buf.WriteString("\n")

	// Add methods
	for _, method := range methodsToAdd {
		buf.WriteString(method)
	}

	// Format and write back
	formatted, err := format.Source(buf.Bytes())
	if err != nil {
		// If formatting fails, write unformatted
		os.WriteFile(filename, buf.Bytes(), 0644)
		fmt.Fprintf(os.Stderr, "Warning: could not format file: %v\n", err)
	} else {
		os.WriteFile(filename, formatted, 0644)
	}
}
