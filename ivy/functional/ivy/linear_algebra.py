# global
from typing import Union, Optional, Tuple, Literal, List, NamedTuple, Sequence

# local
import ivy
from ivy.backend_handler import current_backend
from ivy.func_wrapper import (
    to_native_arrays_and_back,
    handle_out_argument,
    handle_nestable,
)
from ivy.exceptions import handle_exceptions

inf = float("inf")


# Array API Standard #
# -------------------#


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def cholesky(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    upper: Optional[bool] = False,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Computes the cholesky decomposition of the x matrix.

    Parameters
    ----------
    x
        input array having shape (..., M, M) and whose innermost two dimensions form
        square symmetric positive-definite matrices. Should have a floating-point data
        type.
    upper
        If True, the result must be the upper-triangular Cholesky factor U. If False,
        the result must be the lower-triangular Cholesky factor L. Default: False.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the Cholesky factors for each square matrix. If upper is
        False, the returned array must contain lower-triangular matrices; otherwise, the
        returned array must contain upper-triangular matrices. The returned array must
        have a floating-point data type determined by Type Promotion Rules and must have
        the same shape as x.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.cholesky.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`ivy.Array` input:

    >>> x = ivy.array([[4.0, 1.0, 2.0, 0.5, 2.0], \
                       [1.0, 0.5, 0.0, 0.0, 0.0], \
                       [2.0, 0.0, 3.0, 0.0, 0.0], \
                       [0.5, 0.0, 0.0, 0.625, 0.0], \
                       [2.0, 0.0, 0.0, 0.0, 16.0]])
    >>> l = ivy.cholesky(x, upper='false')
    >>> print(l)
    ivy.array([[ 2.  ,  0.5 ,  1.  ,  0.25,  1.  ],
               [ 0.  ,  0.5 , -1.  , -0.25, -1.  ],
               [ 0.  ,  0.  ,  1.  , -0.5 , -2.  ],
               [ 0.  ,  0.  ,  0.  ,  0.5 , -3.  ],
               [ 0.  ,  0.  ,  0.  ,  0.  ,  1.  ]])

    >>> x = ivy.array([[4.0, 1.0, 2.0, 0.5, 2.0], \
                       [1.0, 0.5, 0.0, 0.0, 0.0], \
                       [2.0, 0.0, 3.0, 0.0, 0.0], \
                       [0.5, 0.0, 0.0, 0.625, 0.0], \
                       [2.0, 0.0, 0.0, 0.0, 16.0]])
    >>> y = ivy.zeros([5,5])
    >>> ivy.cholesky(x, upper='false', out=y)
    >>> print(y)
    ivy.array([[ 2.  ,  0.5 ,  1.  ,  0.25,  1.  ],
               [ 0.  ,  0.5 , -1.  , -0.25, -1.  ],
               [ 0.  ,  0.  ,  1.  , -0.5 , -2.  ],
               [ 0.  ,  0.  ,  0.  ,  0.5 , -3.  ],
               [ 0.  ,  0.  ,  0.  ,  0.  ,  1.  ]])

    >>> x = ivy.array([[4.0, 1.0, 2.0, 0.5, 2.0], \
                       [1.0, 0.5, 0.0, 0.0, 0.0], \
                       [2.0, 0.0, 3.0, 0.0, 0.0], \
                       [0.5, 0.0, 0.0, 0.625, 0.0], \
                       [2.0, 0.0, 0.0, 0.0, 16.0]])
    >>> ivy.cholesky(x, upper='false', out=x)
    >>> print(x)
    ivy.array([[ 2.  ,  0.5 ,  1.  ,  0.25,  1.  ],
               [ 0.  ,  0.5 , -1.  , -0.25, -1.  ],
               [ 0.  ,  0.  ,  1.  , -0.5 , -2.  ],
               [ 0.  ,  0.  ,  0.  ,  0.5 , -3.  ],
               [ 0.  ,  0.  ,  0.  ,  0.  ,  1.  ]])

    With :class:`ivy.NativeArray` input:

    >>> x = ivy.array([[1., -2.], [2., 5.]])
    >>> u = ivy.cholesky(x, upper='false')
    >>> print(u)
    ivy.array([[ 1., -2.],
               [ 0.,  1.]])

    With :class:`ivy.Container` input:

    >>> x = ivy.Container(a=ivy.array([[3., -1],[-1., 3.]]), \
                          b=ivy.array([[2., 1.],[1., 1.]]))
    >>> y = ivy.cholesky(x, upper='false')
    >>> print(y)
    {
        a: ivy.array([[1.73, -0.577],
                        [0., 1.63]]),
        b: ivy.array([[1.41, 0.707],
                        [0., 0.707]])
    }

    With multiple :class:`ivy.Container` inputs:

    >>> x = ivy.Container(a=ivy.array([[3., -1],[-1., 3.]]), \
                          b=ivy.array([[2., 1.],[1., 1.]]))
    >>> upper = ivy.Container(a=1, b=-1)
    >>> y = ivy.cholesky(x, upper='false')
    >>> print(y)
    {
        a: ivy.array([[1.73, -0.577],
                        [0., 1.63]]),
        b: ivy.array([[1.41, 0.707],
                        [0., 0.707]])
    }

    With a mix of :class:`ivy.Array` and :class:`ivy.Container` inputs:

    >>> x = ivy.array([[1., -2.], [2., 5.]])
    >>> upper = ivy.Container(a=1, b=-1)
    >>> y = ivy.cholesky(x, upper='false')
    >>> print(y)
    ivy.array([[ 1., -2.],
               [ 0.,  1.]])

    """
    return current_backend(x).cholesky(x, upper=upper, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def cross(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    axisa: int = -1,
    axisb: int = -1,
    axisc: int = -1,
    axis: int = None,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """The cross product of 3-element vectors. If x1 and x2 are multi- dimensional
    arrays (i.e., both have a rank greater than 1), then the cross- product of each pair
    of corresponding 3-element vectors is independently computed.

    Parameters
    ----------
    x1
        first input array. Should have a numeric data type.
    x2
        second input array. Must have the same shape as x1. Should have a numeric data
        type.
    axis
        the axis (dimension) of x1 and x2 containing the vectors for which to compute
        the cross product.vIf set to -1, the function computes the cross product for
        vectors defined by the last axis (dimension). Default: -1.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
         an array containing the cross products. The returned array must have a data
         type determined by Type Promotion Rules.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.cross.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`ivy.Array` inputs:

    >>> x = ivy.array([1., 0., 0.])
    >>> y = ivy.array([0., 1., 0.])
    >>> z = ivy.cross(x, y)
    >>> print(z)
    ivy.array([0., 0., 1.])

    With :class:`ivy.Container` inputs:

    >>> x = ivy.Container(a=ivy.array([5., 0., 0.]), \
                          b=ivy.array([0., 0., 2.]))
    >>> y = ivy.Container(a=ivy.array([0., 7., 0.]), \
                          b=ivy.array([3., 0., 0.]))
    >>> z = ivy.cross(x,y)
    >>> print(z)
    {
        a: ivy.array([0., 0., 35.]),
        b: ivy.array([0., 6., 0.])
    }

    With a combination of :class:`ivy.Array` and :class:`ivy.Container` inputs:

    >>> x = ivy.array([9., 0., 3.])
    >>> y = ivy.Container(a=ivy.array([1., 1., 0.]), \
                          b=ivy.array([1., 0., 1.]))
    >>> z = ivy.cross(x,y)
    >>> print(z)
    {
        a: ivy.array([-3., 3., 9.]),
        b: ivy.array([0., -6., 0.])
    }
    """
    return current_backend(x1).cross(
        x1, x2, axisa=axisa, axisb=axisb, axisc=axisc, axis=axis, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def det(
    x: Union[ivy.Array, ivy.NativeArray], /, *, out: Optional[ivy.Array] = None
) -> ivy.Array:
    """Returns the determinant of a square matrix (or a stack of square matrices)``x``.

    Parameters
    ----------
    x
        input array having shape ``(..., M, M)`` and whose innermost two dimensions
        form square matrices. Should have a floating-point data type.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        if ``x`` is a two-dimensional array, a zero-dimensional array containing the
        determinant; otherwise,a non-zero dimensional array containing the determinant
        for each square matrix. The returned array must have the same data type as
        ``x``.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.det.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Functional Examples
    -------------------
    With :class:`ivy.Array` input:

    >>> x = ivy.array([[2.,4.],[6.,7.]])
    >>> y = ivy.det(x)
    >>> print(y)
    ivy.array(-10.)

    >>> x = ivy.array([[3.4,-0.7,0.9],[6.,-7.4,0.],[-8.5,92,7.]])
    >>> y = ivy.det(x)
    >>> print(y)
    ivy.array(293.46997)

    With :class:`ivy.NativeArray` input:

    >>> x = ivy.native_array([[3.4,-0.7,0.9],[6.,-7.4,0.],[-8.5,92,7.]])
    >>> y = ivy.det(x)
    >>> print(y)
    ivy.array(293.46997)

    With :class:`ivy.Container` input:

    >>> x = ivy.Container(a = ivy.array([[3., -1.], [-1., 3.]]) , \
                                 b = ivy.array([[2., 1.], [1., 1.]]))
    >>> y = ivy.det(x)
    >>> print(y)
    {a:ivy.array(8.),b:ivy.array(1.)}

    Instance Method Examples
    ------------------------

    Using :class:`ivy.Array` instance method:

    >>> x = ivy.array([[2.,4.],[6.,7.]])
    >>> y = x.det()
    >>> print(y)
    ivy.array(-10.)

    Using :class:`ivy.Container` instance method:

    >>> x = ivy.Container(a = ivy.array([[3., -1.], [-1., 3.]]) , \
                                    b = ivy.array([[2., 1.], [1., 1.]]))
    >>> y = x.det()
    >>> print(y)
    {a:ivy.array(8.),b:ivy.array(1.)}


    """
    return current_backend(x).det(x, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def diag(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    offset: Optional[int] = 0,
    padding_value: Optional[float] = 0,
    align: Optional[str] = "RIGHT_LEFT",
    num_rows: Optional[int] = None,
    num_cols: Optional[int] = None,
    out: Optional[ivy.Array] = None,
):
    return current_backend(x).diag(
        x,
        offset=offset,
        padding_value=padding_value,
        align=align,
        num_rows=num_rows,
        num_cols=num_cols,
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def diagonal(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    offset: int = 0,
    axis1: int = -2,
    axis2: int = -1,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns the specified diagonals of a matrix (or a stack of matrices) ``x``.

    Parameters
    ----------
    x
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form
        ``MxN`` matrices.
    offset
        offset specifying the off-diagonal relative to the main diagonal.
        - ``offset = 0``: the main diagonal.
        - ``offset > 0``: off-diagonal above the main diagonal.
        - ``offset < 0``: off-diagonal below the main diagonal.
        Default: `0`.
    axis1
        axis to be used as the first axis of the 2-D sub-arrays from which the diagonals
        should be taken.
        Defaults to first axis (-2).
    axis2
        axis to be used as the second axis of the 2-D sub-arrays from which the
        diagonals should be taken. Defaults to second axis (-1).
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    out
        optional output array to write the result in. Must have the same number
        of dimensions as the function output.

    Returns
    -------
    ret
        an array containing the diagonals and whose shape is determined by removing the
        last two dimensions and appending a dimension equal to the size of the resulting
        diagonals. The returned array must have the same data type as ``x``.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.diagonal.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Functional Examples
    ------------------

    With :class:`ivy.Array` inputs:

    >>> x = ivy.array([[1., 2.],\
                       [3., 4.]])

    >>> d = ivy.diagonal(x)
    >>> print(d)
    ivy.array([1., 4.])


    >>> x = ivy.array([[[1., 2.],\
                        [3., 4.]],\
                       [[5., 6.],\
                        [7., 8.]]])
    >>> d = ivy.diagonal(x)
    >>> print(d)
    ivy.array([[1., 4.],
               [5., 8.]])

    >>> x = ivy.array([[1., 2.],\
                       [3., 4.]])

    >>> d = ivy.diagonal(x, offset=1)
    >>> print(d)
    ivy.array([2.])


    >>> x = ivy.array([[0, 1, 2],\
                       [3, 4, 5],\
                       [6, 7, 8]])
    >>> d = ivy.diagonal(x, offset=-1, axis1=0)
    >>> print(d)
    ivy.array([3, 7])

    >>> x = ivy.array([[[ 0,  1,  2],\
                        [ 3,  4,  5],\
                        [ 6,  7,  8]],\
                       [[ 9, 10, 11],\
                        [12, 13, 14],\
                        [15, 16, 17]],\
                       [[18, 19, 20],\
                        [21, 22, 23],\
                        [24, 25, 26]]])
    >>> d = ivy.diagonal(x, offset=1, axis1=-3)
    >>> print(d)
    ivy.array([[1, 11],
               [4, 14],
               [7, 17]])

    >>> x = ivy.array([[[0, 1],\
                        [2, 3]],\
                       [[4, 5],\
                        [6, 7]]])
    >>> d = ivy.diagonal(x, offset=0, axis1=0, axis2=1)
    >>> print(d)
    ivy.array([[0, 6],
               [1, 7]])

    >>> x = ivy.array([[[1., 2.],\
                        [3., 4.]],\
                       [[5., 6.],\
                        [7., 8.]]])
    >>> d = ivy.diagonal(x, offset=1, axis1=0, axis2=1)
    >>> print(d)
    ivy.array([[3.],
               [4.]])

    With :class:`ivy.NativeArray` inputs:

    >>> x = ivy.native_array([[1., 2.],\
                              [3., 4.]])
    >>> d = ivy.diagonal(x)
    >>> print(d)
    ivy.array([1., 4.])

    >>> x = ivy.native_array([[[ 0,  1,  2],\
                               [ 3,  4,  5],\
                               [ 6,  7,  8]],\
                              [[ 9, 10, 11],\
                               [12, 13, 14],\
                               [15, 16, 17]],\
                              [[18, 19, 20],\
                               [21, 22, 23],\
                               [24, 25, 26]]])
    >>> d = ivy.diagonal(x, offset=1, axis1=1, axis2=-1)
    >>> print(d)
    ivy.array([[ 1,  5],
               [10, 14],
               [19, 23]])

    >>> x = ivy.native_array([[0, 1, 2],\
                              [3, 4, 5],\
                              [6, 7, 8]])
    >>> d = ivy.diagonal(x)
    >>> print(d)
    ivy.array([0, 4, 8])


    With :class:`ivy.Container` inputs:

    >>> x = ivy.Container(\
            a = ivy.array([[7, 1, 2],\
                           [1, 3, 5],\
                           [0, 7, 4]]),\
            b = ivy.array([[4, 3, 2],\
                           [1, 9, 5],\
                           [7, 0, 6]])\
        )
    >>> d = ivy.diagonal(x)
    >>> print(d)
    {
        a: ivy.array([7, 3, 4]),
        b: ivy.array([4, 9, 6])
    }
    """
    return current_backend(x).diagonal(
        x, offset=offset, axis1=axis1, axis2=axis2, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def eigh(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    UPLO: Optional[str] = "L",
    out: Optional[ivy.Array] = None,
) -> NamedTuple:
    """Returns an eigendecomposition x = QLQᵀ of a symmetric matrix (or a stack of
    symmetric matrices) ``x``, where ``Q`` is an orthogonal matrix (or a stack of
    matrices) and ``L`` is a vector (or a stack of vectors).

    .. note::
       The function ``eig`` will be added in a future version of the specification, as
       it requires complex number support, once complex numbers are supported,
       each square matrix must be Hermitian.

    .. note::
       Whether an array library explicitly checks whether an input array is a symmetric
       matrix (or a stack of symmetric matrices) is implementation-defined.

    Parameters
    ----------
    x
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form
        square matrices. Must have a floating-point data type.

    Returns
    -------
    ret
        a namedtuple (``eigenvalues``, ``eigenvectors``) whose

        -   first element must have the field name ``eigenvalues`` (corresponding to
            ``L`` above) and must be an array consisting of computed eigenvalues. The
            array containing the eigenvalues must have shape ``(..., M)``.
        -   second element have have the field name ``eigenvectors`` (corresponding to
            ``Q`` above) and must be an array where the columns of the inner most
            matrices contain the computed eigenvectors. These matrices must be
            orthogonal. The array containing the eigenvectors must have shape
            ``(..., M, M)``.

        -   Each returned array must have the same floating-point data type as ``x``.

    .. note::
       Eigenvalue sort order is left unspecified and is thus implementation-dependent.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.eigh.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).eigh(x, UPLO=UPLO, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def eigvalsh(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    UPLO: Optional[str] = "L",
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Return the eigenvalues of a symmetric matrix (or a stack of symmetric matrices) x.

    .. note::
       The function ``eig`` will be added in a future version of the specification, as
       it requires complex number support, once complex numbers are supported,
       each square matrix must be Hermitian.

    .. note::
       Whether an array library explicitly checks whether an input array is a symmetric
       matrix (or a stack of symmetric matrices) is implementation-defined.

    Parameters
    ----------
    x
        input array having shape (..., M, M) and whose innermost two dimensions form
        square matrices. Must have floating-point data type.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the computed eigenvalues. The returned array must have shape
        (..., M) and have the same data type as x.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.eigvalsh.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).eigvalsh(x, UPLO=UPLO, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def inner(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns the inner product of two vectors ``x1`` and ``x2``.

    Parameters
    ----------
    x1
        first one-dimensional input array of size N. Should have a numeric data type.
        a(N,) array_like
        First input vector. Input is flattened if not already 1-dimensional.
    x2
        second one-dimensional input array of size M. Should have a numeric data type.
        b(M,) array_like
        Second input vector. Input is flattened if not already 1-dimensional.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        a two-dimensional array containing the inner product and whose shape is (N, M).
        The returned array must have a data type determined by Type Promotion Rules.

    """
    return current_backend(x1, x2).inner(x1, x2, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def inv(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    adjoint: bool = False,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns the multiplicative inverse of a square matrix (or a stack of square
    matrices) ``x``.

    Parameters
    ----------
    x
        input array having shape ``(..., M, M)`` and whose innermost two dimensions form
        square matrices. Should have a floating-point data type.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the multiplicative inverses. The returned array must have a
        floating-point data type determined by :ref:`type-promotion` and must have the
        same shape as ``x``.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.inv.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`ivy.Array` inputs:

    >>> x = ivy.array([[1.0, 2.0], [3.0, 4.0]])
    >>> y = ivy.zeros(3)
    >>> ivy.inv(x, out=y)
    >>> print(y)
    ivy.array([[-2., 1.],[1.5, -0.5]])

    Using inplace

    >>> x = ivy.array([[1.0, 2.0], [5.0, 5.0]])
    >>> ivy.inv(x, out=x)
    >>> print(x)
    ivy.array([[-1., 0.4],[1., -0.2]])

    Inverses of several matrices can be computed at once:

    >>> x = ivy.array([[[1.0, 2.0],[3.0, 4.0]],\
                       [[1.0, 3.0], [3.0, 5.0]]])
    >>> y = ivy.inv(x)
    >>> print(y)
    ivy.array([[[-2., 1.],[1.5, -0.5]],
               [[-1.25, 0.75],[0.75, -0.25]]])

    With :class:`ivy.Container` inputs

    >>> x = ivy.Container(a=ivy.array([[11., 100., 10.],\
                        [300., 40., 20.], [25., 30, 100.]]),\
                        b=ivy.array([[4., 400., 50.], [10., 10., 15.],\
                        [50., 5000., 40.]]), c=ivy.array([[25., 22., 100.],\
                        [55, 20., 20.], [55., 50., 100.]]))
    >>> y = ivy.Container.static_inv(x)
    >>> print(y)
    {
        a: ivy.array([[-0.0012, 0.00342, -0.000565],
                      [0.0104, -0.0003, -0.000981],
                      [-0.00282, -0.000766, 0.0104]]),
        b: ivy.array([[-0.0322, 0.101, 0.00237],
                      [0.000151, -0.00101, 0.00019],
                      [0.0214, 0., -0.00171]]),
        c: ivy.array([[0.0107, 0.03, -0.0167],
                      [-0.0472, -0.0322, 0.0536],
                      [0.0177, -0.000429, -0.00762]])

    }

    """
    return current_backend(x).inv(x, adjoint=adjoint, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def matmul(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    transpose_a: bool = False,
    transpose_b: bool = False,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Computes the matrix product.

    Parameters
    ----------
    x1
        first input array. Should have a numeric data type. Must have at least one
        dimension.
    x2
        second input array. Should have a numeric data type. Must have at least one
        dimension.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        -   if both x1 and x2 are one-dimensional arrays having shape (N,), a
            zero-dimensional array containing the inner product as its only element.

        -   if x1 is a two-dimensional array having shape (M, K) and x2 is a
            two-dimensional array having shape (K, N), a two-dimensional array

            containing the conventional matrix product and having shape (M, N).
        -   if x1 is a one-dimensional array having shape (K,) and x2 is an array having
            shape (..., K, N), an array having shape (..., N) (i.e., prepended
            dimensions during vector-to-matrix promotion must be removed) and containing
            the conventional matrix product.

        -   if x1 is an array having shape (..., M, K) and x2 is a one-dimensional array
            having shape (K,), an array having shape (..., M) (i.e., appended dimensions
            during vector-to-matrix promotion must be removed) and containing the
            conventional matrix product.

        -   if x1 is a two-dimensional array having shape (M, K) and x2 is an array
            having shape (..., K, N), an array having shape (..., M, N) and containing
            the conventional matrix product for each stacked matrix.

        -   if x1 is an array having shape (..., M, K) and x2 is a two-dimensional array
            having shape (K, N), an array having shape (..., M, N) and containing the
            conventional matrix product for each stacked matrix.

        -   if either x1 or x2 has more than two dimensions, an array having a shape
            determined by Broadcasting shape(x1)[:-2] against shape(x2)[:-2] and
            containing the conventional matrix product for each stacked matrix.


    **Raises**

        -   if either x1 or x2 is a zero-dimensional array.

        -   if x1 is a one-dimensional array having shape (K,), x2 is a one-dimensional

            array having shape (L,), and K != L.

        -   if x1 is a one-dimensional array having shape (K,), x2 is an array having shape
            (..., L, N), and K != L.

        -   if x1 is an array having shape (..., M, K), x2 is a one-dimensional array having
            shape (L,), and K != L.

        -   if x1 is an array having shape (..., M, K), x2 is an array having shape
            (..., L, N), and K != L.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/API_specification/generated/signatures.linear_algebra_functions.matmul.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :class:`ivy.Array` inputs:

    >>> x = ivy.array([2., 0., 3.])
    >>> y = ivy.array([4., 1., 8.])
    >>> z = ivy.matmul(x, y)
    >>> print(z)
    ivy.array(32.)

    With :class:`ivy.NativeArray` inputs:

    >>> x = ivy.native_array([[1., 2.], [0., 1.]])
    >>> y = ivy.native_array([[2., 0.], [0., 3.]])
    >>> z = ivy.matmul(x, y)
    >>> print(z)
    ivy.array([[2., 6.],[0., 3.]])

    With :class:`ivy.Container` inputs:

    >>> x = ivy.Container(a=ivy.array([5., 1.]), b=ivy.array([1., 0.]))
    >>> y = ivy.Container(a=ivy.array([4., 7.]), b=ivy.array([3., 0.]))
    >>> z = ivy.matmul(x,y)
    >>> print(z)
    {
        a: ivy.array(27.),
        b: ivy.array(3.)
    }

    With a combination of :class:`ivy.Array`
    and :class:`ivy.Container` inputs:

    >>> x = ivy.array([9., 0.])
    >>> y = ivy.Container(a=ivy.array([2., 1.]), b=ivy.array([1., 0.]))
    >>> z = ivy.matmul(x, y)
    >>> print(z)
    {
        a: ivy.array(18.),
        b: ivy.array(9.)
    }

    With a combination of :class:`ivy.NativeArray` and :class:`ivy.Array` inputs:

    >>> x = ivy.native_array([[1., 2.], [0., 3.]])
    >>> y = ivy.array([[1.], [3.]])
    >>> z = ivy.matmul(x, y)
    >>> print(z)
    ivy.array([[7.],[9.]])

    """
    return current_backend(x1).matmul(
        x1, x2, transpose_a=transpose_a, transpose_b=transpose_b, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def matrix_norm(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    ord: Optional[Union[int, float, Literal[inf, -inf, "fro", "nuc"]]] = "fro",
    axis: Optional[Tuple[int, int]] = (-2, -1),
    keepdims: bool = False,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Compute the matrix p-norm.

    Parameters
    ----------
    x
        Input array.
    ord
        Order of the norm. Default is "fro".
    keepdims
        If this is set to True, the axes which are normed over are left in the result as
        dimensions with size one. With this option the result will broadcast correctly
        against the original x. Default is False.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        Matrix norm of the array at specified axes.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.matrix_norm.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).matrix_norm(
        x, ord=ord, axis=axis, keepdims=keepdims, out=out
    )


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def matrix_power(
    x: Union[ivy.Array, ivy.NativeArray], n: int, /, *, out: Optional[ivy.Array] = None
) -> ivy.Array:
    """Raises a square matrix (or a stack of square matrices) x to an integer power n.

    Parameters
    ----------
        x
            input array having shape (..., M, M) and whose innermost two dimensions form square matrices.
            Should have a floating-point data type.
        n
            integer exponent.

    Returns
    -------
        ret
            if n is equal to zero, an array containing the identity matrix for each square matrix.
            If n is less than zero, an array containing the inverse of each square matrix raised to the absolute value of n,
            provided that each square matrix is invertible.
            If n is greater than zero, an array containing the result of raising each square matrix to the power n.
            The returned array must have the same shape as x and a floating-point data type determined by Type Promotion Rules.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.matrix_power.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).matrix_power(x, n, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def matrix_rank(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    atol: Optional[Union[float, Tuple[float]]] = None,
    rtol: Optional[Union[float, Tuple[float]]] = None,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns the rank (i.e., number of non-zero singular values) of a matrix (or a
    stack of matrices).

    Parameters
    ----------
    x
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form
        ``MxN`` matrices. Should have a floating-point data type.

    atol
        absolute tolerance. When None it’s considered to be zero.

    rtol
        relative tolerance for small singular values. Singular values approximately less
        than or equal to ``rtol * largest_singular_value`` are set to zero. If a
        ``float``, the value is equivalent to a zero-dimensional array having a
        floating-point data type determined by :ref:`type-promotion` (as applied to
        ``x``) and must be broadcast against each matrix. If an ``array``, must have a
        floating-point data type and must be compatible with ``shape(x)[:-2]`` (see
        :ref:`broadcasting`). If ``None``, the default value is ``max(M, N) * eps``,
        where ``eps`` must be the machine epsilon associated with the floating-point
        data type determined by :ref:`type-promotion` (as applied to ``x``).
        Default: ``None``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the ranks. The returned array must have a floating-point
        data type determined by :ref:`type-promotion` and must have shape ``(...)``
        (i.e., must have a shape equal to ``shape(x)[:-2]``).


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.matrix_rank.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :code: 'ivy.Array' inputs:

    1. Full Matrix

    >>> x = ivy.array([[1., 2.], [3., 4.]])
    >>> ivy.matrix_rank(x)
    ivy.array(2.)

    2. Rank Deficient Matrix

    >>> x = ivy.array([[1., 0.], [0., 0.]])
    >>> ivy.matrix_rank(x)
    ivy.array(1.)

    3. 1 Dimension - rank 1 unless all 0

    >>> x = ivy.array([[1., 1.])
    >>> ivy.matrix_rank(x)
    ivy.array(1.)

    >>> x = ivy.array([[0., 0.])
    >>> ivy.matrix_rank(x)
    ivy.array(0)

    With :code: 'ivy.NativeArray' inputs:

    >>> x = ivy.native_array([[1., 2.], [3., 4.]], [[1., 0.], [0., 0.]])
    >>> ivy.matrix_rank(x)
    ivy.array([2., 1.])

    With :code: 'ivy.Container' inputs:
    >>> x = ivy.Container(a = ivy.array([[1., 2.], [3., 4.]]) ,
                            b = ivy.array([[1., 0.], [0., 0.]]))
    >>> ivy.matrix_rank(x)
    {
        a:ivy.array(2.),
        b:ivy.array(1.)
    }


    """
    return current_backend(x).matrix_rank(x, atol=atol, rtol=rtol, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def matrix_transpose(
    x: Union[ivy.Array, ivy.NativeArray], /, *, out: Optional[ivy.Array] = None
) -> ivy.Array:
    """Transposes a matrix (or a stack of matrices) ``x``.

    Parameters
    ----------
    x
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form
        ``MxN`` matrices.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the transpose for each matrix and having shape
        ``(..., N, M)``. The returned array must have the same data type as ``x``.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/API_specification/generated/signatures.linear_algebra_functions.matrix_transpose.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).matrix_transpose(x, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def outer(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns the outer product of two vectors ``x1`` and ``x2``.

    Parameters
    ----------
    x1
        first one-dimensional input array of size N. Should have a numeric data type.
        a(N,) array_like
        First input vector. Input is flattened if not already 1-dimensional.
    x2
        second one-dimensional input array of size M. Should have a numeric data type.
        b(M,) array_like
        Second input vector. Input is flattened if not already 1-dimensional.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        a two-dimensional array containing the outer product and whose shape is (N, M).
        The returned array must have a data type determined by Type Promotion Rules.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.outer.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    >>> x = ivy.array([[1., 2.],[3., 4.]])
    >>> y = ivy.array([[5., 6.],[7., 8.]])
    >>> d = ivy.outer(x,y)
    >>> print(d)
    ivy.array([[ 5.,  6.,  7.,  8.],
                [10., 12., 14., 16.],
                [15., 18., 21., 24.],
                [20., 24., 28., 32.]])

    >>> d = ivy.outer(x, 1)
    >>> print(d)
    ivy.array([[1.],
                [2.],
                [3.],
                [4.]])

    A 3-D Example

    >>> x = ivy.array([[[1., 2.],\
                        [3., 4.]],\
                       [[5., 6.],\
                        [7., 8.]]])
    >>> y = ivy.array([[[9., 10.],\
                        [11., 12.]],\
                       [[13., 14.],\
                        [15., 16.]]])
    >>> d = ivy.outer(x, y)
    >>> print(d)
    ivy.array([[  9.,  10.,  11.,  12.,  13.,  14.,  15.,  16.],
                [ 18.,  20.,  22.,  24.,  26.,  28.,  30.,  32.],
                [ 27.,  30.,  33.,  36.,  39.,  42.,  45.,  48.],
                [ 36.,  40.,  44.,  48.,  52.,  56.,  60.,  64.],
                [ 45.,  50.,  55.,  60.,  65.,  70.,  75.,  80.],
                [ 54.,  60.,  66.,  72.,  78.,  84.,  90.,  96.],
                [ 63.,  70.,  77.,  84.,  91.,  98., 105., 112.],
                [ 72.,  80.,  88.,  96., 104., 112., 120., 128.]])

    """
    return current_backend(x1, x2).outer(x1, x2, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def pinv(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    rtol: Optional[Union[float, Tuple[float]]] = None,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns the (Moore-Penrose) pseudo-inverse of a matrix (or a stack of matrices)
    ``x``.

    Parameters
    ----------
    x
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form
        ``MxN`` matrices. Should have a floating-point data type.
    rtol
        relative tolerance for small singular values. Singular values approximately less
        than or equal to ``rtol * largest_singular_value`` are set to zero. If a
        ``float``, the value is equivalent to a zero-dimensional array having a
        floating-point data type determined by :ref:`type-promotion` (as applied to
        ``x``) and must be broadcast against each matrix. If an ``array``, must have a
        floating-point data type and must be compatible with ``shape(x)[:-2]``
        (see :ref:`broadcasting`). If ``None``, the default value is
        ``max(M, N) * eps``, where ``eps`` must be the machine epsilon associated with
        the floating-point data type determined by :ref:`type-promotion` (as applied to
        ``x``). Default: ``None``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the pseudo-inverses. The returned array must have a
        floating-point data type determined by :ref:`type-promotion` and must have shape
        ``(..., N, M)`` (i.e., must have the same shape as ``x``, except the innermost
        two dimensions must be transposed).


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.pinv.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    >>> x = ivy.array([[1., 2.],[3., 4.]])
    >>> y = ivy.pinv(x)
    >>> print(y)
    ivy.array([[-2., 1.],[1.5, -0.5]])

    >>> x = ivy.array([[1., 2.],[3., 4.]])
    >>> out = ivy.zeros(x.shape)
    >>> ivy.pinv(x, out=out)
    >>> print(out)
    ivy.array([[-2., 1.],[1.5, -0.5]])

    """
    return current_backend(x).pinv(x, rtol=rtol, out=out)


@to_native_arrays_and_back
@handle_nestable
@handle_exceptions
def qr(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    mode: str = "reduced",
) -> NamedTuple:
    """
    Returns the qr decomposition x = QR of a full column rank matrix (or a stack of
    matrices), where Q is an orthonormal matrix (or a stack of matrices) and R is an
    upper-triangular matrix (or a stack of matrices).

    Parameters
    ----------
    x
        input array having shape (..., M, N) and whose innermost two dimensions form MxN
        matrices of rank N. Should have a floating-point data type.
    mode
        decomposition mode. Should be one of the following modes:
        - 'reduced': compute only the leading K columns of q, such that q and r have
          dimensions (..., M, K) and (..., K, N), respectively, and where K = min(M, N).
        - 'complete': compute q and r with dimensions (..., M, M) and (..., M, N),
          respectively.
        Default: 'reduced'.

    Returns
    -------
    ret
        a namedtuple (Q, R) whose
        - first element must have the field name Q and must be an array whose shape
          depends on the value of mode and contain matrices with orthonormal columns.
          If mode is 'complete', the array must have shape (..., M, M). If mode is
          'reduced', the array must have shape (..., M, K), where K = min(M, N). The
          first x.ndim-2 dimensions must have the same size as those of the input array
          x.
        - second element must have the field name R and must be an array whose shape
          depends on the value of mode and contain upper-triangular matrices. If mode is
          'complete', the array must have shape (..., M, N). If mode is 'reduced', the
          array must have shape (..., K, N), where K = min(M, N). The first x.ndim-2
          dimensions must have the same size as those of the input x.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.qr.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).qr(x, mode=mode)


@to_native_arrays_and_back
@handle_nestable
@handle_exceptions
def slogdet(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
) -> NamedTuple:
    """Computes the sign and natural logarithm of the determinant of an array.

    Parameters
    ----------
    x
        input array having shape (..., M, M) and whose innermost two dimensions form
        square matrices. Should have a floating-point data type.

    Returns
    -------
    ret
        This function returns NamedTuple with two values -
            sign:
            An array containing a number representing the sign of the determinant
            for each square matrix.

            logabsdet:
            An array containing natural log of the absolute determinant of each
            square matrix.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :code:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    With :code:`ivy.Array` input:

    >>> x = ivy.array([[1.0, 2.0], \
                       [3.0, 4.0]])
    >>> y = ivy.slogdet(x)
    >>> print(y)
    slogdet(sign=ivy.array(-1.), logabsdet=ivy.array(0.6931472))

    With :code:`ivy.Container` input:

    >>> x = ivy.Container(a=ivy.array([[1.0, 2.0],   \
                                       [3.0, 4.0]]), \
                          b=ivy.array([[1.0, 2.0],   \
                                       [2.0, 1.0]]))
    >>> y = ivy.slogdet(x)
    >>> print(y)
    {
        a: (list[2], <class ivy.array.array.Array> shape=[]),
        b: (list[2], <class ivy.array.array.Array> shape=[])
    }


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.slogdet.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).slogdet(x)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def solve(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """
    Returns the solution to the system of linear equations represented by the well-
    determined (i.e., full rank) linear matrix equation AX = B.

    Parameters
    ----------
    x1
        coefficient array A having shape (..., M, M) and whose innermost two dimensions
        form square matrices. Must be of full rank (i.e., all rows or, equivalently,
        columns must be linearly independent). Should have a floating-point data type.
    x2
        ordinate (or “dependent variable”) array B. If x2 has shape (M,), x2 is
        equivalent to an array having shape (..., M, 1). If x2 has shape (..., M, K),
        each column k defines a set of ordinate values for which to compute a solution,
        and shape(x2)[:-1] must be compatible with shape(x1)[:-1] (see Broadcasting).
        Should have a floating-point data type.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the solution to the system AX = B for each square matrix.
        The returned array must have the same shape as x2 (i.e., the array corresponding
        to B) and must have a floating-point data type determined by Type Promotion
        Rules.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.solve.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x1, x2).solve(x1, x2, out=out)


@to_native_arrays_and_back
@handle_nestable
@handle_exceptions
def svd(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    compute_uv: bool = True,
    full_matrices: bool = True,
) -> Union[ivy.Array, Tuple[ivy.Array, ...]]:
    """Returns a singular value decomposition A = USVh of a matrix (or a stack of
    matrices) ``x``, where ``U`` is a matrix (or a stack of matrices) with orthonormal
    columns, ``S`` is a vector of non-negative numbers (or stack of vectors), and ``Vh``
    is a matrix (or a stack of matrices) with orthonormal rows.


    Parameters
    ----------
    x
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form
        matrices on which to perform singular value decomposition. Should have a
        floating-point data type.
    full_matrices
        If ``True``, compute full-sized ``U`` and ``Vh``, such that ``U`` has shape
        ``(..., M, M)`` and ``Vh`` has shape ``(..., N, N)``. If ``False``, compute on
        the leading ``K`` singular vectors, such that ``U`` has shape ``(..., M, K)``
        and ``Vh`` has shape ``(..., K, N)`` and where ``K = min(M, N)``.
        Default: ``True``.
    compute_uv
        If ``True`` then left and right singular vectors will be computed and returned
        in ``U`` and ``Vh``, respectively. Otherwise, only the singular values will be computed,
        which can be significantly faster.
    .. note::
        with backend set as torch, svd with still compute left and right singular vectors irrespective
        of the value of compute_uv, however Ivy will still only return the singular values.

    Returns
    -------
    .. note::
        once complex numbers are supported, each square matrix must be Hermitian.

    ret
        a namedtuple ``(U, S, Vh)`` whose

        -   first element must have the field name ``U`` and must be an array whose
            shape depends on the value of ``full_matrices`` and contain matrices with
            orthonormal columns (i.e., the columns are left singular vectors). If
            ``full_matrices`` is ``True``, the array must have shape ``(..., M, M)``.
            If ``full_matrices`` is ``False``, the array must have shape
            ``(..., M, K)``, where ``K = min(M, N)``. The first ``x.ndim-2`` dimensions
            must have the same shape as those of the input ``x``.
        -   second element must have the field name ``S`` and must be an array with
            shape ``(..., K)`` that contains the vector(s) of singular values of length
            ``K``, where ``K = min(M, N)``. For each vector, the singular values must be
            sorted in descending order by magnitude, such that ``s[..., 0]`` is the
            largest value, ``s[..., 1]`` is the second largest value, et cetera. The
            first ``x.ndim-2`` dimensions must have the same shape as those of the input
            ``x``.
        -   third element must have the field name ``Vh`` and must be an array whose
            shape depends on the value of ``full_matrices`` and contain orthonormal rows
            (i.e., the rows are the right singular vectors and the array is the
            adjoint). If ``full_matrices`` is ``True``, the array must have shape
            ``(..., N, N)``. If ``full_matrices`` is ``False``, the array must have
            shape ``(..., K, N)`` where ``K = min(M, N)``. The first ``x.ndim-2``
            dimensions must have the same shape as those of the input ``x``.

        Each returned array must have the same floating-point data type as ``x``.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.svd.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Examples
    --------
    >>> x = ivy.random_normal(shape = (9, 6))
    >>> U, S, Vh = ivy.svd(x)
    >>> print(U.shape, S.shape, Vh.shape)
    (9, 9) (6,) (6, 6)

    Reconstruction from SVD, result is numerically close to x

    >>> reconstructed_x = ivy.matmul(U[:,:6] * S, Vh)
    >>> print((reconstructed_x - x > 1e-3).sum())
    ivy.array(0)

    >>> print((reconstructed_x - x < -1e-3).sum())
    ivy.array(0)

    >>> x = ivy.random_normal(shape = (9, 6))
    >>> S = ivy.svd(x, compute_uv = False)
    print(S)

    """
    return current_backend(x).svd(x, compute_uv=compute_uv, full_matrices=full_matrices)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def svdvals(
    x: Union[ivy.Array, ivy.NativeArray], /, *, out: Optional[ivy.Array] = None
) -> ivy.Array:
    """Returns the singular values of a matrix (or a stack of matrices) ``x``.

    Parameters
    ----------
    x
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form
        ``MxN`` matrices.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        array with shape ``(..., K)`` that contains the vector(s) of singular values of
        length ``K``, where K = min(M, N). The values are sorted in descending order by
        magnitude.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.svdvals.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Functional Examples
    -------------------

    With :class:`ivy.Array` input:

    >>> x = ivy.array([[5.0, 7.0], [4.0, 3.0]])
    >>> S = ivy.svdvals(x)
    >>> print(S.shape)
    (2,)

    Compare the singular value S by ivy.svdvals() with the result by ivy.svd().

    >>> _, SS, _ = ivy.svd(x)
    >>> print(SS.shape)
    (2,)

    >>> error = (SS - S).abs()
    >>> print(error)
    ivy.array([0.,0.])

    With :class:`ivy.NativeArray` input:

    >>> x = ivy.native_array([[1.0, 2.0, 3.0], [2.0, 3.0, 4.0],\
                              [2.0, 1.0, 3.0], [3.0, 4.0, 5.0]])
    >>> print(x.shape)
    (4, 3)

    >>> S = ivy.svdvals(x)
    >>> print(S)
    ivy.array([10.3, 1.16, 0.615])

    >>> _, SS, _ = ivy.svd(x)
    >>> print(SS)
    ivy.array([10.3, 1.16, 0.615])

    Compare the singular value S by ivy.svdvals() with the result by ivy.svd().

    >>> error = (SS - S).abs()
    >>> print(error)
    ivy.array([0., 0., 0.])

    With :class:`ivy.Container` input:

    >>> x = ivy.Container(a=ivy.array([[2.0, 3.0], [3.0, 4.0],\
                                       [1.0, 3.0], [3.0, 5.0]]),\
                          b=ivy.array([[7.0, 1.0, 2.0, 3.0],\
                                       [2.0, 5.0, 3.0, 4.0],\
                                       [2.0, 6.0, 1.0, 3.0],\
                                       [3.0, 4.0, 5.0, 9.0]]))
    >>> y = ivy.svdvals(x)
    >>> print(y)
    {
        a: ivy.array([9.01, 0.866]),
        b: ivy.array([15.8, 5.56, 4.17, 0.864])
    }

    Instance Method Examples
    ------------------------

    Using :class:`ivy.Array` instance method:

    >>> x = ivy.array([[8.0, 3.0], [2.0, 3.0],\
                       [2.0, 1.0], [3.0, 4.0],\
                       [4.0, 1.0], [5.0, 6.0]])
    >>> y = x.svdvals()
    >>> print(y)
    ivy.array([13.4, 3.88])

    Using :class:`ivy.Container` instance method:

    >>> x = ivy.Container(a=ivy.array([[2.0, 3.0, 6.0], [5.0, 3.0, 4.0],\
                                       [1.0, 7.0, 3.0], [3.0, 2.0, 5.0]]),\
                          b=ivy.array([[7.0, 1.0, 2.0, 3.0, 9.0],\
                                       [2.0, 5.0, 3.0, 4.0, 10.0],\
                                       [2.0, 11.0, 6.0, 1.0, 3.0],\
                                       [8.0, 3.0, 4.0, 5.0, 9.0]]))
    >>> y = x.svdvals()
    >>> print(y)
    {
        a: ivy.array([13., 4.64, 2.55]),
        b: ivy.array([23.2, 10.4, 4.31, 1.36])
    }

    """
    return current_backend(x).svdvals(x, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def tensordot(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    axes: Union[int, Tuple[List[int], List[int]]] = 2,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns a tensor contraction of x1 and x2 over specific axes.

    Parameters
    ----------
    x1
        First input array. Should have a numeric data type.
    x2
        second input array. Must be compatible with x1 for all non-contracted axes.
        Should have a numeric data type.
    axes
        The axes to contract over.
        Default is 2.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        The tensor contraction of x1 and x2 over the specified axes.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/API_specification/generated/signatures.linear_algebra_functions.tensordot.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    Functional Examples
    -------------------
    With :class:`ivy.Array` input:

    >>> x = ivy.array([[1., 2.], [2., 3.]])
    >>> y = ivy.array([[3., 4.], [4., 5.]])
    >>> res = ivy.tensordot(x, y, axes =0)
    >>> print(res)
    ivy.array([[[[3.,4.],[4.,5.]],[[6.,8.],[8.,10.]]],[[[6.,8.],[8.,10.]],[[9.,12.],[12.,15.]]]])

    With a mix of :class:`ivy.Array` and :class:`ivy.NativeArray` inputs:

    >>> x = ivy.array([[1., 0., 1.], [2., 3., 6.], [0., 7., 2.]])
    >>> y = ivy.native_array([[1.], [2.], [3.]])
    >>> res = ivy.tensordot(x, y, axes = 1)
    >>> print(res)
    ivy.array([[ 4.],
                [26.],
                [20.]])

    With :class:`ivy.Container` input:

    >>> x = ivy.Container(a=ivy.array([[1., 0., 3.], [2., 3., 4.]]),\
                          b=ivy.array([[5., 6., 7.], [3., 4., 8.]]))
    >>> y = ivy.Container(a=ivy.array([[2., 4., 5.], [9., 10., 6.]]),\
                          b=ivy.array([[1., 0., 3.], [2., 3., 4.]]))
    >>> res = ivy.tensordot(x, y)
    >>> print(res)
    {
        a: ivy.array(89.),
        b: ivy.array(76.)
    }


    """
    return current_backend(x1, x2).tensordot(x1, x2, axes=axes, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def trace(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    offset: int = 0,
    axis1: int = 0,
    axis2: int = 1,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Returns the sum along the specified diagonals of a matrix (or a stack of
    matrices) ``x``.

    Parameters
    ----------
    x
        input array having shape ``(..., M, N)`` and whose innermost two dimensions form
        ``MxN`` matrices. Should have a numeric data type.
    offset
        offset specifying the off-diagonal relative to the main diagonal.
        -   ``offset = 0``: the main diagonal.
        -   ``offset > 0``: off-diagonal above the main diagonal.
        -   ``offset < 0``: off-diagonal below the main diagonal.

        Default: ``0``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
         an array containing the traces and whose shape is determined by removing the
         last two dimensions and storing the traces in the last array dimension. For
         example, if ``x`` has rank ``k`` and shape ``(I, J, K, ..., L, M, N)``, then an
         output array has rank ``k-2`` and shape ``(I, J, K, ..., L)`` where

         ::

           out[i, j, k, ..., l] = trace(a[i, j, k, ..., l, :, :])

         The returned array must have the same data type as ``x``.

    Examples
    --------
    With :class:`ivy.Array` inputs:

    >>> x = ivy.array([[2., 0., 3.],\
                        [3., 5., 6.]])
    >>> y = ivy.trace(x, offset=0)
    >>> print(y)
    ivy.array(7.)

    >>> x = ivy.array([[[1., 2.],\
                        [3., 4.]],\
                       [[5., 6.],\
                        [7., 8.]]])
    >>> y = ivy.trace(x, offset=1)
    >>> print(y)
    ivy.array([3., 4.])

    With :class:`ivy.NativeArray` inputs:

    >>> x = ivy.native_array([[2., 0., 3.],[3., 5., 6.]])
    >>> y = ivy.trace(x, offset=0)
    >>> print(y)
    ivy.array(7.)

    >>> x = ivy.native_array([[0, 1, 2],\
                              [3, 4, 5],\
                              [6, 7, 8]])
    >>> y = ivy.trace(x, offset=0)
    >>> print(y)
    ivy.array(12)

    With :class:`ivy.Container` inputs:

    >>> x = ivy.Container(\
            a = ivy.array([[7, 1, 2],\
                           [1, 3, 5],\
                           [0, 7, 4]]),\
            b = ivy.array([[4, 3, 2],\
                           [1, 9, 5],\
                           [7, 0, 6]])\
        )
    >>> y = ivy.trace(x, offset=0)
    >>> print(y)
    {
        a: ivy.array(14),
        b: ivy.array(19)
    }

    >>> x = ivy.Container(\
            a = ivy.array([[7, 1, 2],\
                           [1, 3, 5],\
                           [0, 7, 4]]),\
            b = ivy.array([[4, 3, 2],\
                           [1, 9, 5],\
                           [7, 0, 6]])\
        )
    >>> y = ivy.trace(x, offset=1)
    >>> print(y)
    {
        a: ivy.array(6),
        b: ivy.array(8)
    }
    """
    return current_backend(x).trace(x, offset=offset, axis1=axis1, axis2=axis2, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def vecdot(
    x1: Union[ivy.Array, ivy.NativeArray],
    x2: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    axis: int = -1,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Computes the (vector) dot product of two arrays.

    Parameters
    ----------
    x1
        first input array. Should have a numeric data type.
    x2
        second input array. Must be compatible with ``x1`` (see :ref:`broadcasting`).
        Should have a numeric data type.
    axis
        axis over which to compute the dot product. Must be an integer on the interval
        ``[-N, N)``, where ``N`` is the rank (number of dimensions) of the shape
        determined according to :ref:`broadcasting`. If specified as a negative integer,
        the function must determine the axis along which to compute the dot product by
        counting backward from the last dimension (where ``-1`` refers to the last
        dimension). By default, the function must compute the dot product over the last
        axis. Default: ``-1``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        if ``x1`` and ``x2`` are both one-dimensional arrays, a zero-dimensional
        containing the dot product; otherwise, a non-zero-dimensional array containing
        the dot products and having rank ``N-1``, where ``N`` is the rank (number of
        dimensions) of the shape determined according to :ref:`broadcasting`. The
        returned array must have a data type determined by :ref:`type-promotion`.


    **Raises**

        -   if provided an invalid ``axis``.

        -   if the size of the axis over which to compute the dot product is not the same
            for both ``x1`` and ``x2``.



    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/API_specification/generated/signatures.linear_algebra_functions.vecdot.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x1).vecdot(x1, x2, axis=axis, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def vector_norm(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    axis: Optional[Union[int, Sequence[int]]] = None,
    keepdims: bool = False,
    ord: Union[int, float, Literal[inf, -inf]] = 2,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    r"""Computes the vector norm of a vector (or batch of vectors) ``x``.

    Parameters
    ----------
    x
        input array. Should have a floating-point data type.
    axis
        If an integer, ``axis`` specifies the axis (dimension) along which to compute
        vector norms. If an n-tuple, ``axis`` specifies the axes (dimensions) along
        which to compute batched vector norms. If ``None``, the vector norm must be
        computed over all array values (i.e., equivalent to computing the vector norm of
        a flattened array). Negative indices must be supported. Default: ``None``.
    keepdims
        If ``True``, the axes (dimensions) specified by ``axis`` must be included in the
        result as singleton dimensions, and, accordingly, the result must be compatible
        with the input array (see :ref:`broadcasting`). Otherwise, if ``False``, the
        axes (dimensions) specified by ``axis`` must not be included in the result.
        Default: ``False``.
    ord
        order of the norm. The following mathematical norms must be supported:

        +------------------+----------------------------+
        | ord              | description                |
        +==================+============================+
        | 1                | L1-norm (Manhattan)        |
        +------------------+----------------------------+
        | 2                | L2-norm (Euclidean)        |
        +------------------+----------------------------+
        | inf              | infinity norm              |
        +------------------+----------------------------+
        | (int,float >= 1) | p-norm                     |
        +------------------+----------------------------+

        The following non-mathematical "norms" must be supported:

        +------------------+--------------------------------+
        | ord              | description                    |
        +==================+================================+
        | 0                | sum(a != 0)                    |
        +------------------+--------------------------------+
        | -1               | 1./sum(1./abs(a))              |
        +------------------+--------------------------------+
        | -2               | 1./sqrt(sum(1./abs(a)\*\*2))   |
        +------------------+--------------------------------+
        | -inf             | min(abs(a))                    |
        +------------------+--------------------------------+
        | (int,float < 1)  | sum(abs(a)\*\*ord)\*\*(1./ord) |
        +------------------+--------------------------------+

        Default: ``2``.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        an array containing the vector norms. If ``axis`` is ``None``, the returned
        array must be a zero-dimensional array containing a vector norm. If ``axis`` is
        a scalar value (``int`` or ``float``), the returned array must have a rank which
        is one less than the rank of ``x``. If ``axis`` is a ``n``-tuple, the returned
        array must have a rank which is ``n`` less than the rank of ``x``. The returned
        array must have a floating-point data type determined by :ref:`type-promotion`.


    This function conforms to the `Array API Standard
    <https://data-apis.org/array-api/latest/>`_. This docstring is an extension of the
    `docstring <https://data-apis.org/array-api/latest/extensions/generated/signatures.linalg.vector_norm.html>`_ # noqa
    in the standard.

    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(x).vector_norm(
        x, axis=axis, keepdims=keepdims, ord=ord, out=out
    )


# Extra #
# ------#


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def vector_to_skew_symmetric_matrix(
    vector: Union[ivy.Array, ivy.NativeArray], /, *, out: Optional[ivy.Array] = None
) -> ivy.Array:
    """Given vector, return the associated skew-symmetric matrix
    `[reference] <https://en.wikipedia.org/wiki/Skew-symmetric_matrix#Cross_product>`_

    Parameters
    ----------
    vector
        Vector to convert *[batch_shape,3]*.
    out
        optional output array, for writing the result to. It must have a shape that the
        inputs broadcast to.

    Returns
    -------
    ret
        Skew-symmetric matrix *[batch_shape,3,3]*.


    Both the description and the type hints above assumes an array input for simplicity,
    but this function is *nestable*, and therefore also accepts :class:`ivy.Container`
    instances in place of any of the arguments.

    """
    return current_backend(vector).vector_to_skew_symmetric_matrix(vector, out=out)


@to_native_arrays_and_back
@handle_out_argument
@handle_nestable
@handle_exceptions
def vander(
    x: Union[ivy.Array, ivy.NativeArray],
    /,
    *,
    N: Optional[int] = None,
    increasing: Optional[bool] = False,
    out: Optional[ivy.Array] = None,
) -> ivy.Array:
    """Generates a Vandermonde matrix.
    The columns of the output matrix are elementwise powers
    of the input vector x^{(N-1)}, x^{(N-2)}, ..., x^0x. 
    If increasing is True, the order of the columns is reversed 
    x^0, x^1, ..., x^{(N-1)}. Such a matrix with a geometric progression 
    in each row is named for Alexandre-Theophile Vandermonde.

    Parameters
    ----------
    x
        1-D input array.
    N
         Number of columns in the output. If N is not specified,
         a square array is returned (N = len(x))
    increasing 
        Order of the powers of the columns. If True, the powers increase
        from left to right, if False (the default) they are reversed.
    out
        optional output array, for writing the result to.

    Returns
    -------
    ret
        Vandermonde matrix.

    Examples
    --------
    
    With :class:`ivy.Array` inputs:

    >>> x = ivy.array([1, 2, 3, 5])
    >>> ivy.vander(x)
    ivy.array(
       [[  1,   1,   1,   1],
        [  8,   4,   2,   1],
        [ 27,   9,   3,   1],
        [125,  25,   5,   1]]
        )

    >>> x = ivy.array([1, 2, 3, 5])
    >>> ivy.vander(x, N=3)
    ivy.array(
       [[ 1,  1,  1],
        [ 4,  2,  1],
        [ 9,  3,  1],
        [25,  5,  1]]
        )

    >>> x = ivy.array([1, 2, 3, 5])
    >>> ivy.vander(x, N=3, increasing=True)
    ivy.array(
       [[ 1,  1,  1],
        [ 1,  2,  4],
        [ 1,  3,  9],
        [ 1,  5, 25]]
        )
    """
    return current_backend().vander(
        x, N=N, increasing=increasing, out=out
    )
