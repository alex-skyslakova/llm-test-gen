// version 1.1.3
 
object MD5 {
 
    private val INIT_A = 0x67452301
    private val INIT_B = 0xEFCDAB89L.toInt()
    private val INIT_C = 0x98BADCFEL.toInt()
    private val INIT_D = 0x10325476
 
    private val SHIFT_AMTS = intArrayOf(
        7, 12, 17, 22,
        5,  9, 14, 20,
        4, 11, 16, 23,
        6, 10, 15, 21
    )
 
    private val TABLE_T = IntArray(64) {
        ((1L shl 32) * Math.abs(Math.sin(it + 1.0))).toLong().toInt()
    }
 
    fun compute(message: ByteArray): ByteArray {
        val messageLenBytes = message.size
        val numBlocks = ((messageLenBytes + 8) ushr 6) + 1
        val totalLen = numBlocks shl 6
        val paddingBytes = ByteArray(totalLen - messageLenBytes)
        paddingBytes[0] = 0x80.toByte()
        var messageLenBits = (messageLenBytes shl 3).toLong()
 
        for (i in 0..7) {
            paddingBytes[paddingBytes.size - 8 + i] = messageLenBits.toByte()
            messageLenBits = messageLenBits ushr 8
        }
 
        var a = INIT_A
        var b = INIT_B
        var c = INIT_C
        var d = INIT_D
        val buffer = IntArray(16)
 
        for (i in 0 until numBlocks) {
            var index = i shl 6
 
            for (j in 0..63) {
                val temp = if (index < messageLenBytes) message[index] else 
                               paddingBytes[index - messageLenBytes]
                buffer[j ushr 2] = (temp.toInt() shl 24) or (buffer[j ushr 2] ushr 8) 
                index++
            }
 
            val originalA = a
            val originalB = b
            val originalC = c
            val originalD = d
 
            for (j in 0..63) {
                val div16 = j ushr 4
                var f = 0
                var bufferIndex = j
                when (div16) {
                    0 -> {
                        f = (b and c) or (b.inv() and d)
                    }
 
                    1 -> {
                        f = (b and d) or (c and d.inv()) 
                        bufferIndex = (bufferIndex * 5 + 1) and 0x0F
                    }
 
                    2 -> {
                        f = b xor c xor d;
                        bufferIndex = (bufferIndex * 3 + 5) and 0x0F
                    }
 
                    3 -> {
                        f = c xor (b or d.inv());
                        bufferIndex = (bufferIndex * 7) and 0x0F
                    }
                } 
 
                val temp = b + Integer.rotateLeft(a + f + buffer[bufferIndex] + 
                           TABLE_T[j], SHIFT_AMTS[(div16 shl 2) or (j and 3)])
                a = d
                d = c
                c = b
                b = temp
            }
 
            a += originalA
            b += originalB
            c += originalC
            d += originalD
        }   
 
        val md5 = ByteArray(16)
        var count = 0
 
        for (i in 0..3) {
            var n = if (i == 0) a else (if (i == 1) b else (if (i == 2) c else d))
 
            for (j in 0..3) {      
                md5[count++] = n.toByte()
                n = n ushr 8
            }
        }
        return md5
    }
}
 
fun ByteArray.toHexString(): String {
    val sb = StringBuilder()
    for (b in this) sb.append(String.format("%02x", b.toInt() and 0xFF))
    return sb.toString()
}
 
fun main(args: Array<String>) {
    val testStrings = arrayOf(
        "",
        "a",
        "abc",
        "message digest",
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890"
    )
 
    println("${"hash code".padStart(34)} <== string") 
    for (s in testStrings) {
        println("0x${MD5.compute(s.toByteArray()).toHexString()} <== \"$s\"")
    }
}