#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/arrayobject.h>

#include <vector>
#include <cstring>
#include <slime.h>

bool inline checkNarg(int64_t lNarg, int64_t lNargExp)
{
    if (lNarg != lNargExp)
    {
        printf("wrong num. of arg, narg=%ld, %ld expected\n", lNarg, lNargExp);
        abort();
        return false;
    }
    return true;
}

static PyObject* genPhant_py(PyObject* self, PyObject* const* args, Py_ssize_t nargs)
{
    checkNarg(nargs,4);
    int64_t nAx = PyLong_AsLongLong(args[0]);
    int64_t nPix = PyLong_AsLongLong(args[1]);
    double ampRes = PyFloat_AsDouble(args[2]);
    double ampCar = PyFloat_AsDouble(args[3]);

    // Generate into std::vector
    std::vector<uint8_t> vu8Phant;
    genPhant(nAx, nPix, ampRes, ampCar, &vu8Phant);

    // convert vector to numpy array
    PyObject* pPyObj_Arr;
    {
        npy_intp aDims[] = {nPix, nPix, nPix};
        pPyObj_Arr = PyArray_ZEROS(nAx, aDims, NPY_UINT8, 0);
    }

    // fill the data in
    std::memcpy(PyArray_DATA((PyArrayObject*)pPyObj_Arr),
                vu8Phant.data(),
                vu8Phant.size() * sizeof(uint8_t));

    return pPyObj_Arr;
}

static PyMethodDef aMeth[] =
{
    {"genPhant", (PyCFunction)genPhant_py, METH_FASTCALL, "genPhant(nAx, nPix, ampRes, ampCar) -> np.ndarray[uint8]"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef sMod =
{
    PyModuleDef_HEAD_INIT,
    "ext",
    NULL,
    -1,
    aMeth
};

PyMODINIT_FUNC PyInit_ext(void)
{
    import_array();  // required for NumPy C-API
    return PyModule_Create(&sMod);
}