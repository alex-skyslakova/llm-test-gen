import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

class FreeCellGameTest {

    @Test
    fun testGame1() {
        val expectedOutput = """
            Game #1:
            JD  2D  9H  JC  5D  7H  7C  5H  
            KD  KC  9S  5S  AD  QC  KH  3H  
            2S  KS  9D  QD  JS  AS  AH  3C  
            4C  5C  TS  QH  4H  AC  4D  7S  
            3S  TD  4S  TH  8H  2C  JH  7D  
            6D  8S  8D  QS  6C  3D  8C  TC  
            6S  9C  2H  6H  

        """.trimIndent()

        val outputStream = java.io.ByteArrayOutputStream()
        System.setOut(java.io.PrintStream(outputStream))

        game(1)

        assertEquals(expectedOutput, outputStream.toString().trim())
    }

    @Test
    fun testGame617() {
        val expectedOutput = """
            Game #617:
            7D  AD  5C  3S  5S  8C  2D  AH  
            TD  7S  QD  AC  6D  8H  AS  KH  
            TH  QC  3H  9D  6S  8D  3D  TC  
            KD  5H  9S  3C  8S  7H  4D  JS  
            4C  QS  9C  9H  7C  6H  2C  2S  
            4S  TS  2H  5D  JC  6C  JH  QH  
            JD  KS  KC  4H  

        """.trimIndent()

        val outputStream = java.io.ByteArrayOutputStream()
        System.setOut(java.io.PrintStream(outputStream))

        game(617)

        assertEquals(expectedOutput, outputStream.toString().trim())
    }

    @Test
    fun testInvalidDealNumber() {
        val exception = assertThrows(IllegalArgumentException::class.java) {
            game(0)
        }
        assertEquals("Failed requirement.", exception.message)
    }
}