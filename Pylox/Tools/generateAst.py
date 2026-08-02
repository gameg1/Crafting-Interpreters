import sys
from typing import TextIO

SPACE_4 = "    "
SPACE_8 = "        "

def main():
    if (len(sys.argv) != 2):
        print("Usage: generateAst <output directory>")
        exit(64)

    outputDir:str = sys.argv[1]

    _defineAst(outputDir, "Expr", [
        "Assign   | name: Token, value: Expr",
        "Binary   | left: Expr, operator: Token, right: Expr",
        "Grouping | expression: Expr",
        "Literal  | value",
        "Unary    | operator: Token, right: Expr",
        "Variable | name: Token"
    ])

    _defineAst(outputDir, "Stmt", [
        "Expression | expression: Expr",
        "print      | expression: Expr",
        "Var        | name: Token, initializer: Expr"
    ])

def _defineAst(outputDir:str, baseName:str, types:list[str])-> None:
    path:str = outputDir + "/" + baseName + ".py"
    output_writer = open(path,"w", encoding="UTF-8")

    _defineVisitor(output_writer, baseName, types)

    for type in types:
        className:str = type.split("|", 1)[0].strip()
        fields:str = type.split("|", 1)[1].strip()
        _defineType(output_writer, baseName, className, fields)

def _defineVisitor(writer:TextIO, baseName:str, types:list[str]):
    writer.write('V = TypeVar("V")\n\n\n')
    writer.write("class Visitor(ABC, Generic[V]):\n")

    for type in types:
        typeName:str = type.split(":")[0].strip()
        writer.write(f"{SPACE_4}@abstractmethod\n")
        writer.write(f"{SPACE_4}def visit_{typeName.lower()}_{baseName.lower()}"
                     f'(self, {baseName.lower()}: " {typeName}") -> V: ...\n'
                     )

def _defineType(writer: TextIO, baseName:str, className:str, fieldList:str):
    writer.write("\n\n")
    writer.write(f"class {className}({baseName}):\n")
    # Follow 80 char limit
    if len(fieldList) < 55:
        writer.write(f"    def __init__(self, {fieldList}):\n")
    elif len (fieldList) < 65:
        writer.write("    def __init__(\n")
        writer.write("        self, " + fieldList)
        writer.write("\n    ):\n")
    else:
        writer.write("    def __init__(\n        )")
        writer.write(",\n        ".join(["self"] + fieldList.split(", ")))
        writer.write(",\n    ):\n")
    
    field_list = fieldList.split(", ")
    for field in field_list:
        name = field.strip()
        writer.write(f"{SPACE_8}self.{name} = {name.split(':')[0]}\n")
    writer.write("\n")

    writer.write(f"{SPACE_4}def accept(self, visitor: Visitor):\n")
    writer.write(
        f"{SPACE_8}return visitor.visit_" f"{className.lower()}_{baseName.lower()}(self)\n"
    )

if __name__ == "__main__":
    main()