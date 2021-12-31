# Frida rpm builder

Simplified and (hopefully) more operating system independent way to build Frida
rpm for Fedora 35. This might be useful until
https://github.com/frida/frida/issues/1967 is resolved.

## How to

Run:
```
git clone --recurse-submodules https://github.com/frida/frida frida

podman build -t frida-build-ubuntu -f Containerfile

podman run -ti -v ./frida:/src --workdir=/src --user "$(id -u):$(id -g)" --userns=keep-id frida-build-ubuntu python3.10 /build/build_rpm.py
```

and rpms will be available under:
```
frida/frida-{python,tools}/build/rpm/*.rpm
```

rpm cleanup:
```
rm -f frida/frida-{python,tools}/build/rpm/*.rpm
```

Frida cleanup:

```
podman run -ti -v ./frida:/src --workdir=/src --user "$(id -u):$(id -g)" --userns=keep-id frida-build-ubuntu make clean
```

## References

* https://github.com/frida/frida
* https://frida.re/
