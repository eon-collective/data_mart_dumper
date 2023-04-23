from re import S
from src.pg_dumper import quote_swap

def test_quote_swap_double():
    """Test that a swap happens correctly when provided a string
       with double quotes and swap out is double."""
    myStr_string = "hello, what is your \"name\""
    swap_out='double'

    swapped_out = quote_swap(myStr_string, swap_out)
    assert swapped_out == "hello, what is your 'name'"

def test_quote_swap_single():
    """Test that a swap happens correctly when provided a string
       with single quotes and swap out is single."""
    myStr_string = "hello, what is your 'name'"
    swap_out='single'

    swapped_out = quote_swap(myStr_string, swap_out)
    assert swapped_out == "hello, what is your \"name\""

