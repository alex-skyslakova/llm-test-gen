package main

import (
	"reflect"
	"testing"
)

func TestFilter(t *testing.T) {
	tests := []struct {
		name     string
		filter   filter
		input    []float64
		expected []float64
	}{
		{
			name: "Test Butterworth filter on given signal",
			filter: filter{
				a: []float64{1.00000000, -2.77555756e-16, 3.33333333e-01, -1.85037171e-17},
				b: []float64{0.16666667, 0.5, 0.5, 0.16666667},
			},
			input: []float64{
				-0.917843918645, 0.141984778794, 1.20536903482, 0.190286794412,
				-0.662370894973, -1.00700480494, -0.404707073677, 0.800482325044,
				0.743500089861, 1.01090520172, 0.741527555207, 0.277841675195,
				0.400833448236, -0.2085993586, -0.172842103641, -0.134316096293,
				0.0259303398477, 0.490105989562, 0.549391221511, 0.9047198589,
			},
			expected: []float64{
				-0.152973986441, -0.116476523579, 0.366648476215, 0.515923755481,
				0.233612139929, -0.374315663365, -0.563156204641, -0.107061138656,
				0.486787119498, 0.764998276582, 0.755788073372, 0.568011446707,
				0.422266187919, 0.202477026062, 0.019391702421, -0.066947281840,
				0.010671755737, 0.246930444774, 0.478315186696, 0.667946686579,
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			output := tt.filter.filter(tt.input)
			if !reflect.DeepEqual(output, tt.expected) {
				t.Errorf("expected %v, got %v", tt.expected, output)
			}
		})
	}
}
