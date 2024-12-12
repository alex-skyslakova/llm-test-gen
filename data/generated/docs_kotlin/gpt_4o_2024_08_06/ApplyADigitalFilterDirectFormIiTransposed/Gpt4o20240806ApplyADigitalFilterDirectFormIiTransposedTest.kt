import org.junit.jupiter.api.Assertions.assertArrayEquals
import org.junit.jupiter.api.Test

class ApplyADigitalFilterDirectFormIiTransposedTest {

    @Test
    fun testFilter() {
        val a = doubleArrayOf(1.00000000, -2.77555756e-16, 3.33333333e-01, -1.85037171e-17)
        val b = doubleArrayOf(0.16666667, 0.5, 0.5, 0.16666667)

        val signal = doubleArrayOf(
            -0.917843918645, 0.141984778794, 1.20536903482, 0.190286794412,
            -0.662370894973, -1.00700480494, -0.404707073677, 0.800482325044,
            0.743500089861, 1.01090520172, 0.741527555207, 0.277841675195,
            0.400833448236, -0.2085993586, -0.172842103641, -0.134316096293,
            0.0259303398477, 0.490105989562, 0.549391221511, 0.9047198589
        )

        val expected = doubleArrayOf(
            -0.15297399, -0.38793652, 0.04553192, 0.53033184,
            0.16838470, -0.55893682, -0.69302857, -0.17864898,
            0.26071013, 0.78607562, 0.98601482, 0.84472191,
            0.56906489, 0.27899381, 0.05209718, -0.02685070,
            0.06260197, 0.28767998, 0.57963588, 0.78538464
        )

        val result = filter(a, b, signal)
        assertArrayEquals(expected, result, 1e-8)
    }
}
