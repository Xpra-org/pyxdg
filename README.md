The XDG Package contains:

    - Implementation of the XDG-Base-Directory Standard
      http://standards.freedesktop.org/basedir-spec/

    - Implementation of the XDG-Desktop Standard
      http://standards.freedesktop.org/desktop-entry-spec/

    - Implementation of the XDG-Menu Standard
      http://standards.freedesktop.org/menu-spec/

    - Implementation of the XDG-Icon-Theme Standard
      http://standards.freedesktop.org/icon-theme-spec/

    - Implementation of the XDG-Shared MIME-info Database
      http://standards.freedesktop.org/shared-mime-info-spec/

    - Implementation of the XDG-Recent File Storage Specification
      http://standards.freedesktop.org/recent-file-spec/

To run the tests, run pytest in the top level directory.

## About this fork

This is a fork of PyXDG, maintained by the Xpra project:
https://github.com/Xpra-org/pyxdg

The original project is maintained by Thomas Kluyver and the freedesktop.org
community:

  - Homepage: http://freedesktop.org/wiki/Software/pyxdg
  - Source:   https://gitlab.freedesktop.org/xdg/pyxdg
              (mirrored at https://github.com/takluyver/pyxdg)
  - Mailing list: xdg@lists.freedesktop.org

This fork only exists because upstream appears to be inactive (the last release,
0.28, was in June 2022) and we need working packages for recent distributions
and Python versions.
We will happily delete this fork once work resumes upstream.
