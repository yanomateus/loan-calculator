def linear_service_fee(principal, fee):
    """Calculate service fee proportional to the principal.

    If :math:`S` is the principal and :math:`g` is the fee aliquot, then the
    fee is given by :math:`gS`.
    """

    return float(principal * fee)
