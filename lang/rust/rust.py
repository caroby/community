from typing import Any, Callable, TypeVar

from talon import Context, Module, actions, settings

from ..tags.operators import Operators

mod = Module()
# rust specific grammar
mod.list("code_type_modifier", desc="List of type modifiers for active language")
mod.list("code_macros", desc="List of macros for active language")
mod.list("code_trait", desc="List of traits for active language")


@mod.action_class
class Actions:
    def code_state_implements():
        """Inserts implements block, positioning the cursor appropriately"""

    def code_insert_macro(text: str, selection: str):
        """Inserts a macro and positions the cursor appropriately"""

    def code_insert_macro_array(text: str, selection: str):
        """Inserts a macro array and positions the cursor appropriately"""

    def code_insert_macro_block(text: str, selection: str):
        """Inserts a macro block and positions the cursor appropriately"""

    def code_state_unsafe():
        """Inserts an unsafe block and positions the cursor appropriately"""

    def code_comment_documentation_block():
        """Inserts a block document comment and positions the cursor appropriately"""

    def code_comment_documentation_inner():
        """Inserts an inner document comment and positions the cursor appropriately"""

    def code_comment_documentation_block_inner():
        """Inserts an inner block document comment and positions the cursor appropriately"""


ctx = Context()
ctx.matches = r"""
code.language: rust
"""

scalar_types = {
    "eye eight": "i8",
    "you eight": "u8",
    "bytes": "u8",
    "eye sixteen": "i16",
    "you sixteen": "u16",
    "eye thirty two": "i32",
    "you thirty two": "u32",
    "eye sixty four": "i64",
    "you sixty four": "u64",
    "eye one hundred and twenty eight": "i128",
    "you one hundred and twenty eight": "u128",
    "eye size": "isize",
    "you size": "usize",
    "float thirty two": "f32",
    "float sixty four": "f64",
    "boolean": "bool",
    "character": "char",
}

compound_types = {
    "tuple": "()",
    "array": "[]",
}

standard_library_types = {
    "box": "Box",
    "vector": "Vec",
    "string": "String",
    "string slice": "&str",
    "os string": "OsString",
    "os string slice": "&OsStr",
    "see string": "CString",
    "see string slice": "&CStr",
    "option": "Option",
    "result": "Result",
    "hashmap": "HashMap",
    "hash set": "HashSet",
    "reference count": "Rc",
}

standard_sync_types = {
    "arc": "Arc",
    "barrier": "Barrier",
    "condition variable": "Condvar",
    "mutex": "Mutex",
    "once": "Once",
    "read write lock": "RwLock",
    "receiver": "Receiver",
    "sender": "Sender",
    "sink sender": "SyncSender",
}

all_types = {
    **scalar_types,
    **compound_types,
    **standard_library_types,
    **standard_sync_types,
}

standard_function_macros = {
    "panic": "panic!",
    "format": "format!",
    "concatenate": "concat!",
    "print": "print!",
    "print line": "println!",
    "error print line": "eprintln!",
    "to do": "todo!",
}

standard_array_macros = {
    "vector": "vec!",
}

standard_block_macros = {
    "macro rules": "macro_rules!",
}

logging_macros = {
    "debug": "debug!",
    "info": "info!",
    "warning": "warn!",
    "error": "error!",
}

testing_macros = {
    "assert": "assert!",
    "assert equal": "assert_eq!",
    "assert not equal": "assert_ne!",
}

all_function_macros = {
    **standard_function_macros,
    **logging_macros,
    **testing_macros,
}

all_array_macros = {
    **standard_array_macros,
}

all_block_macros = {
    **standard_block_macros,
}

all_macros = {
    **all_function_macros,
    **all_array_macros,
    **all_block_macros,
}

all_function_macro_values = set(all_function_macros.values())
all_array_macro_values = set(all_array_macros.values())
all_block_macro_values = set(all_block_macros.values())

closure_traits = {
    "closure": "Fn",
    "closure once": "FnOnce",
    "closure mutable": "FnMut",
}

conversion_traits = {
    "into": "Into",
    "from": "From",
}

iterator_traits = {
    "iterator": "Iterator",
}

all_traits = {
    **closure_traits,
    **conversion_traits,
    **iterator_traits,
}


# tag: libraries
ctx.lists["user.code_libraries"] = {
    "eye oh": "std::io",
    "file system": "std::fs",
    "envy": "std::env",
    "collections": "std::collections",
}

# tag: functions_common
ctx.lists["user.code_common_function"] = {
    "drop": "drop",
    "catch unwind": "catch_unwind",
    "iterator": "iter",
    "into iterator": "into_iter",
    "from iterator": "from_iter",
    **all_macros,
}

# tag: functions
ctx.lists["user.code_type"] = all_types

# rust specific grammar
ctx.lists["user.code_type_modifier"] = {
    "mutable": "mut ",
    "mute": "mut ",
    "borrowed": "&",
    "borrowed mutable": "&mut ",
    "borrowed mute": "&mut ",
    "mutable borrowed": "&mut ",
    "mute borrowed": "&mut ",
}


@ctx.capture("user.code_type", rule="[{user.code_type_modifier}] {user.code_type}")
def code_type(m) -> str:
    """Returns a macro name"""
    return "".join(m)


ctx.lists["user.code_macros"] = all_macros

ctx.lists["user.code_trait"] = all_traits

operators = Operators(
    # code_operators_array
    SUBSCRIPT=lambda: actions.user.insert_between("[", "]"),
    # code_operators_assignment
    ASSIGNMENT=" = ",
    ASSIGNMENT_ADDITION=" += ",
    ASSIGNMENT_SUBTRACTION=" -= ",
    ASSIGNMENT_MULTIPLICATION=" *= ",
    ASSIGNMENT_DIVISION=" /= ",
    ASSIGNMENT_MODULO=" %= ",
    ASSIGNMENT_BITWISE_AND=" &= ",
    ASSIGNMENT_BITWISE_OR=" |= ",
    ASSIGNMENT_BITWISE_EXCLUSIVE_OR=" ^= ",
    ASSIGNMENT_BITWISE_LEFT_SHIFT=" <<= ",
    ASSIGNMENT_BITWISE_RIGHT_SHIFT=" >>= ",
    # code_operators_bitwise
    BITWISE_AND=" & ",
    BITWISE_OR=" | ",
    BITWISE_EXCLUSIVE_OR=" ^ ",
    BITWISE_LEFT_SHIFT=" << ",
    BITWISE_RIGHT_SHIFT=" >> ",
    # code_operators_math
    MATH_ADD=" + ",
    MATH_SUBTRACT=" - ",
    MATH_MULTIPLY=" * ",
    MATH_DIVIDE=" / ",
    MATH_MODULO=" % ",
    MATH_EXPONENT=lambda: actions.user.insert_between(".pow(", ")"),
    MATH_EQUAL=" == ",
    MATH_NOT_EQUAL=" != ",
    MATH_GREATER_THAN=" > ",
    MATH_GREATER_THAN_OR_EQUAL=" >= ",
    MATH_LESS_THAN=" < ",
    MATH_LESS_THAN_OR_EQUAL=" <= ",
    MATH_AND=" && ",
    MATH_OR=" || ",
    ASSIGNMENT_INCREMENT=" += 1",
    # code_operators_pointer
    POINTER_INDIRECTION="*",
    POINTER_ADDRESS_OF="&",
)


@ctx.action_class("user")
class UserActions:
    def code_get_operators() -> Operators:
        return operators

    # tag: imperative

    # tag: object_oriented

    def code_operator_object_accessor():
        actions.auto_insert(".")

    def code_self():
        actions.auto_insert("self")

    def code_define_class():
        actions.user.insert_snippet_by_name("structDeclaration")

    # tag: data_bool

    def code_insert_true():
        actions.auto_insert("true")

    def code_insert_false():
        actions.auto_insert("false")

    # tag: data_null

    def code_insert_null():
        actions.auto_insert("None")

    def code_insert_is_null():
        actions.auto_insert(".is_none()")

    def code_insert_is_not_null():
        actions.auto_insert(".is_some()")

    # tag: functions

    def code_default_function(text: str):
        actions.user.code_private_function(text)

    def code_private_function(text: str):
        actions.auto_insert("fn ")
        formatter = settings.get("user.code_private_function_formatter")
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(function_name, None)

    def code_protected_function(text: str):
        actions.auto_insert("pub(crate) fn ")
        formatter = settings.get("user.code_protected_function_formatter")
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(function_name, None)

    def code_public_function(text: str):
        actions.auto_insert("pub fn ")
        formatter = settings.get("user.code_public_function_formatter")
        function_name = actions.user.formatted_text(text, formatter)
        actions.user.code_insert_function(function_name, None)

    def code_insert_type_annotation(type: str):
        actions.auto_insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.auto_insert(f" -> {type}")

    # tag: functions_gui

    def code_insert_function(text: str, selection: str):
        code_insert_function_or_macro(text, selection, "(", ")")

    # tag: libraries

    def code_insert_library(text: str, selection: str):
        actions.user.insert_snippet_by_name("importStatement", {"0": text})

    # rust specific grammar

    def code_state_implements():
        actions.user.insert_snippet_by_name("implementsStruct")

    def code_insert_macro(text: str, selection: str):
        if text in all_array_macro_values:
            code_insert_function_or_macro(text, selection, "[", "]")
        elif text in all_block_macro_values:
            code_insert_function_or_macro(text, selection, "{", "}")
        else:
            code_insert_function_or_macro(text, selection, "(", ")")

    def code_state_unsafe():
        actions.user.insert_snippet_by_name("unsafeBlock")

    def code_comment_documentation_block():
        actions.user.insert_between("/**", "*/")
        actions.key("enter")

    def code_comment_documentation_inner():
        actions.auto_insert("//! ")

    def code_comment_documentation_block_inner():
        actions.user.insert_between("/*!", "*/")
        actions.key("enter")


def code_insert_function_or_macro(
    text: str,
    selection: str,
    left_delim: str,
    right_delim: str,
):
    if selection:
        out_text = text + f"{left_delim}{selection}{right_delim}"
    else:
        out_text = text + f"{left_delim}{right_delim}"
    actions.user.paste(out_text)
    actions.edit.left()


RT = TypeVar("RT")  # return type


def repeat_call(n: int, f: Callable[..., RT], *args: Any, **kwargs: Any):
    for i in range(n):
        f(*args, **kwargs)
