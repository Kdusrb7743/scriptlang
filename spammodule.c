#include <python.h>
#include <string.h>

// C로 구현한 소스
static PyObject* spam_division(PyObject* self, PyObject* args) {
	int quotient = 0;
	int dividend, divisor = 0;

	if (!PyArg_ParseTuple(args, "ii", &dividend, &divisor))
		return NULL;

	if (divisor) {
		quotient = dividend / divisor;
		return Py_BuildValue("i", quotient);
	}
	else {
		PyErr_SetString(PyExc_ZeroDivisionError, "divisor must not be zero");
		return NULL;
	}
}

static PyObject* spam_strlen(PyObject* self, PyObject* args) {
	char* str;
	int len;

	if (!PyArg_ParseTuple(args, "s", &str))
		return NULL;
	len = strlen(str);
	return Py_BuildValue("i", len);
}

// 모듈 초기화.
static PyMethodDef SpamMethods[] = {
	{"division", spam_division, METH_VARARGS, "division function"},
	{"strlen", spam_strlen, METH_VARARGS, "count a string length."},
	{NULL, NULL, 0, NULL}		// <- 배열 끝 표시.
};

static PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",
	"It is a test module.",
	-1, SpamMethods
};

PyMODINIT_FUNC PyInit_spam(void) {
	return PyModule_Create(&spammodule);
}
