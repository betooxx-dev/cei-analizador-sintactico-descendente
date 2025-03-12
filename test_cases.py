class TestCases:
    @staticmethod
    def get_examples():
        examples = [
            """/ Caso de prueba 1: Declaraciones de variables y asignaciones
int x;
float y;
string message;
x = 10;
y = 3.14;
message = "Hello, world!";
""",
         
            """/ Caso de prueba 2: Sentencia if-else
int number;
number = 42;
if (number > 10) {
    print(number);
} else {
    print(0);
}
""",
         
            """/ Caso de prueba 3: Ciclo while
int counter;
counter = 1;
while (counter <= 5) {
    print(counter);
    counter = counter + 1;
}
""",
         
            """/ Caso de prueba 4: Operaciones de entrada y aritméticas
int a;
int b;
input(a);
input(b);
int sum;
sum = a + b;
int product;
product = a * b;
print(sum);
print(product);
""",
         
            """/ Caso de prueba 5: Este contiene errores de sintaxis
int x;
x = 10;
if x > 5) { / Falta paréntesis de apertura
    print(x)  / Falta punto y coma
}
"""
        ]
        return examples