package queries

import _ "embed"

//go:embed get_by_uid.sql
var GetByUID string

//go:embed list_active_by_search.sql
var ListActiveBySearch string
