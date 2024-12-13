import static org.junit.Assert.assertArrayEquals;
import org.junit.Test;

public class ProductTest {

    @Test
    public void testKroneckerProductSample1() {
        int[][] a = {
            {1, 2},
            {3, 4}
        };
        int[][] b = {
            {0, 5},
            {6, 7}
        };
        int[][] expected = {
            {0, 5, 0, 10},
            {6, 7, 12, 14},
            {0, 15, 0, 20},
            {18, 21, 24, 28}
        };
        assertArrayEquals(expected, Product.product(a, b));
    }

    @Test
    public void testKroneckerProductSample2() {
        int[][] a = {
            {0, 1, 0},
            {1, 1, 1},
            {0, 1, 0}
        };
        int[][] b = {
            {1, 1, 1, 1},
            {1, 0, 0, 1},
            {1, 1, 1, 1}
        };
        int[][] expected = {
            {0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0},
            {0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0},
            {0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0},
            {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
            {1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1},
            {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
            {0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0},
            {0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0},
            {0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0}
        };
        assertArrayEquals(expected, Product.product(a, b));
    }
}