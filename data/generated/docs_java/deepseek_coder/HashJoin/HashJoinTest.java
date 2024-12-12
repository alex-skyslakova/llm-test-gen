import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class HashJoinTest {

    @Test
    public void testHashJoin() {
        String[][] table1 = {
            {"27", "Jonah"},
            {"18", "Alan"},
            {"28", "Glory"},
            {"18", "Popeye"},
            {"28", "Alan"}
        };

        String[][] table2 = {
            {"Jonah", "Whales"},
            {"Jonah", "Spiders"},
            {"Alan", "Ghosts"},
            {"Alan", "Zombies"},
            {"Glory", "Buffy"},
            {"Bob", "foo"}
        };

        List<String[][]> expected = Arrays.asList(
            new String[][]{{"27", "Jonah"}, {"Jonah", "Whales"}},
            new String[][]{{"27", "Jonah"}, {"Jonah", "Spiders"}},
            new String[][]{{"18", "Alan"}, {"Alan", "Ghosts"}},
            new String[][]{{"18", "Alan"}, {"Alan", "Zombies"}},
            new String[][]{{"28", "Glory"}, {"Glory", "Buffy"}},
            new String[][]{{"28", "Alan"}, {"Alan", "Ghosts"}},
            new String[][]{{"28", "Alan"}, {"Alan", "Zombies"}}
        );

        List<String[][]> result = HashJoin.hashJoin(table1, 1, table2, 0);

        assertEquals(expected.size(), result.size());

        for (String[][] expectedRow : expected) {
            boolean found = false;
            for (String[][] resultRow : result) {
                if (Arrays.deepEquals(expectedRow, resultRow)) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                assertEquals(true, false, "Expected row not found: " + Arrays.deepToString(expectedRow));
            }
        }
    }
}
