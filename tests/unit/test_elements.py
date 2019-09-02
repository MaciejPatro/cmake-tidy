import unittest

from cmake_tidy.parsing.elements import PrimitiveElement, ComplexElement


class TestElements(unittest.TestCase):
    def test_empty_primitive_should_print_nothing(self):
        self.assertEqual('', str(PrimitiveElement()))

    def test_primitive_should_hold_name_and_list_of_values(self):
        values = ['abc', 5, 'd']
        name = 'property'

        primitive = PrimitiveElement(name, values)

        self.assertEqual(name, primitive.name)
        self.assertListEqual(values, primitive.values)
        self.assertEqual(f'{name}: {values}', str(primitive))

    def test_complex_element_should_print_nothing_when_empty(self):
        self.assertEqual('', str(ComplexElement()))

    def test_complex_element_should_handle_multiple_primitives(self):
        element = ComplexElement('complex')\
            .add(PrimitiveElement('abc', 123))\
            .add(PrimitiveElement('def', 456))
        self.assertIn('complex.abc: 123', str(element))
        self.assertIn('complex.def: 456', str(element))

    def test_complex_elements_can_be_both_populated_with_primitives_and_complex_elements(self):
        root = ComplexElement('root')
        root.add(PrimitiveElement('abc', 123))
        root.add(ComplexElement('another').add(PrimitiveElement('def', 456)))
        root.add(ComplexElement('empty'))

        self.assertEqual('root.abc: 123\nroot.another.def: 456', str(root))
