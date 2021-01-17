The grossup consists of including due taxes and service fee into a given
principal augmenting it so its resulting net value equals the originally
provided principal. We can also think of the grossed up principal as the
financed value: in onder to grant a loan whose net value exactly matches
the amount demanded by the borrower, it is necessary to finance a greater
amount comprehending services fees and due taxes.

It seems fairly reasonable to assume the service fee is simply an aliquot
applied over the principal so, if :math:`s` is the principal and :math:`\gamma`
is the service fee aliquot, then the service fee given by :math:`\gamma s`. On
the other hand, it is hard to pin down a reasonable and generic expression
for due taxes, since they are very context bound and their rules might be
revised as laws are amended. Therefore, loans being granted in different
contexts will have their principals grossed up by different amounts.

Let us examine the particular case of loans being granted by Brazilian
financial institutions to a natural person. This is ruled by the law-decree
n. 6306, dating December 14th, 2007, for which the relevant parts are
copied and translated below. The amended text can be checked out
`here <http://www.planalto.gov.br/ccivil_03/_Ato2007-2010/2007/Decreto/D6306compilado.htm>`_.

-------------------------


    TÍTULO I

    DA INCIDÊNCIA

    Art. 2o  O IOF incide sobre:

    I - operações de crédito realizadas:

    a) por instituições financeiras (Lei no 5.143, de 20 de outubro de 1966, art. 1o);

    c) entre pessoas jurídicas ou entre pessoa jurídica e pessoa física (Lei no 9.779, de 19 de janeiro de 1999, art. 13);

This excerpt defines our study case as being affected by the IOF law. It
says "The IOF affects I - credit operations performed by a) financial
institutions (...) c) between natural persons or a jurisdictional person
and a natural person.

-------------------------

    TÍTULO II

    DA INCIDÊNCIA SOBRE OPERAÇÕES DE CRÉDITO

    CAPÍTULO I

    DO FATO GERADOR

    Art. 3o  O fato gerador do IOF é a entrega do montante ou do valor que
    constitua o objeto da obrigação, ou sua colocação à disposição do
    interessado (Lei no 5.172, de 1966, art. 63, inciso I).

    § 1o  Entende-se ocorrido o fato gerador e devido o IOF sobre operação de
    crédito:

    I - na data da efetiva entrega, total ou parcial, do valor que constitua o
    objeto da obrigação ou sua colocação à disposição do interessado;

This defines the taxable event (fato gerador) as happening at the date
where the amount constituting the object of obligation is delivered
or made available to the borrowing part.

-------------------------

    CAPÍTULO II

    DOS CONTRIBUINTES E DOS RESPONSÁVEIS

    Dos Contribuintes

    Art. 4o  Contribuintes do IOF são as pessoas físicas ou jurídicas tomadoras
    de crédito (Lei no 8.894, de 1994, art. 3o, inciso I, e Lei no 9.532, de
    1997, art. 58).

    (...)

    Dos Responsáveis

    Art. 5o  São responsáveis pela cobrança do IOF e pelo seu recolhimento ao
    Tesouro Nacional:

    I - as instituições financeiras que efetuarem operações de crédito
    (Decreto-Lei nº 1.783, de 1980, art. 3º, inciso I);

This excerpt defines the jurisdictional or natural person borrowing
money as the taxpayer for the IOF, and the financial institution
providing credit as accountable for collecting the tax and delivering
it to the national treasure.

-------------------------

    CAPÍTULO III

    DA BASE DE CÁLCULO E DA ALÍQUOTA

    Da Alíquota

    Art. 6o  O IOF será cobrado à alíquota máxima de um vírgula cinco por cento
    ao dia sobre o valor das operações de crédito (Lei no 8.894, de 1994, art.
    1o).

    Da Base de Cálculo e das Alíquotas Reduzidas

    Art. 7o  A base de cálculo e respectiva alíquota reduzida do IOF são (Lei
    no 8.894, de 1994, art. 1o, parágrafo único, e Lei no 5.172, de 1966, art.
    64, inciso I):

    I - na operação de empréstimo, sob qualquer modalidade, inclusive abertura
    de crédito:

    (...)

    b) quando ficar definido o valor do principal a ser utilizado pelo
    mutuário, a base de cálculo é o principal entregue ou colocado à sua
    disposição, ou quando previsto mais de um pagamento, o valor do principal
    de cada uma das parcelas:

    1. mutuário pessoa jurídica: 0,0041% ao dia;

    2. mutuário pessoa física: 0,0082% ao dia;

This is, perhaps, the most important excerpt since it defines the
values of the aliquots and describes how to apply them. It states

    1.  that the daily aliquot should not be greater than 1.5%,

    2.  that whenever the loan's principal is well defined (which is our case),
        the calculation basis is the principal (or the amortization) of each
        instalment, the aliquot being 0.0082% per day. Therefore, if the
        :math:`i`-th instalment has amortization :math:`A_i` and is expected to be
        paid :math:`n_i` days after the taxable event, then due amount of IOF is
        given by

        .. math::

            A_i\ \min(n_i \ 0.000082, 0.015)

A last excerpt defines a complementary aliquot to be applied on the principal:

    § 15.  Sem prejuízo do disposto no caput, o IOF incide sobre as operações
    de crédito à alíquota adicional de trinta e oito centésimos por cento,
    independentemente do prazo da operação, seja o mutuário pessoa física ou
    pessoa jurídica.      (Incluído pelo Decreto nº 6.339, de 2008).

It says that "(...) the IOF is applied on credit operations at the aliquot of
thirty eight hundredths per cent regardless of how much time the operation
lasts, be the borrower a natural or jurisdictional person". Therefore, if
:math:`s` is the principal, the due complementary IOF is given by

    .. math::

        s\ 0.0038.

-------------------------

Putting all the pieces together, we arrive at the equation below

.. math::

    s - \sum_{i=1}^k A_i \min(n_i\ 0.0038, 0.015) - s\ 0.0038 - \gamma s = s_\circ

where :math:`s` is the grossed up principal, :math:`A_1,A_2,\ldots,A_k` are the
amortizations, :math:`\gamma` is the sevice fee aliquot and :math:`s_\circ` is
the net principal. Therefore, solving the grossup problem for this specific
scenario, means solving the equation above on :math:`s`.
