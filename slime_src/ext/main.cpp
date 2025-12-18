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
    int64_t lNAx = PyLong_AsLongLong(args[0]);
    int64_t lNPix = PyLong_AsLongLong(args[1]);
    double dResAmp = PyFloat_AsDouble(args[2]);
    double dCarAmp = PyFloat_AsDouble(args[3]);

    // Generate into std::vector
    std::vector<uint8_t> vu8Phant;
    genPhant(lNAx, lNPix, dResAmp, dCarAmp, &vu8Phant);

    // convert vector to numpy array
    PyObject* ppyoNpa;
    {
        npy_intp aDims[] = {lNPix, lNPix, lNPix};
        ppyoNpa = PyArray_ZEROS(lNAx, aDims, NPY_UINT8, 0);
    }

    // fill the data in
    std::memcpy(PyArray_DATA((PyArrayObject*)ppyoNpa),
                vu8Phant.data(),
                vu8Phant.size() * sizeof(uint8_t));

    return ppyoNpa;
}

static PyMethodDef aMeth[] =
{
    {"genPhant", (PyCFunction)genPhant_py, METH_FASTCALL, "genPhant(lNAx, lNPix, dResAmp, dCarAmp) -> np.ndarray[uint8]"},
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