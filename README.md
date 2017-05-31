# h5file-scheme

This is a Taurus scheme that provides access to the contents of hdf5 files
as Taurus Attributes. It uses the [h5py](http://h5py.org) module.

## Enabling
To enable it, install `h5file` and edit `<taurus>/tauruscustomsettings.py`
to add `h5file` to the `EXTRA_SCHEME_MODULES` list. For example:

```python
EXTRA_SCHEME_MODULES = ['h5file']
```

## Examples:

Once the new scheme is enabled in your taurus installation, you can:

- ... get the value of the `foo/bar` dataset from the 
`/path/to/myfile.h5` file with:

```python
import taurus
myattr = taurus.Attribute('h5file:/path/to/myfile.h5::foo/bar')
```
- Show a value from a file in a TaurusForm:

```bash
$> taurusform h5file:/path/to/myfile.h5::foo/bar
```
- Combine h5file attributes with attributes from other
schemes:
```bash
$> taurusform 'h5file:/path/to/myfile.h5::foo/bar' \
              'tango:sys/tg_test/1/float_scalar'\
              'eval:{h5file:/path/to/myfile.h5::foo/bar}*{tango:sys/tg_test/1/ampli}'
```
