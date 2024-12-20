import java.math.BigInteger
 
// version 1.0.5-2
 
fun main(args: Array<String>) {
    // print until 2147483647
    (0..Int.MAX_VALUE).forEach { println(it) }
 
    // print forever
    var n = BigInteger.ZERO
    while (true) {
        println(n)
        n += BigInteger.ONE
    }
}