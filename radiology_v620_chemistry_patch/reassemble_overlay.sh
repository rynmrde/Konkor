#!/usr/bin/env bash
# Reassemble the transport-split Chemistry V6.2 overlay and verify it before extraction.
set -euo pipefail
cd "$(dirname "$0")"
cat overlay.tar.xz.part00 overlay.tar.xz.part01 overlay.tar.xz.part02 overlay.tar.xz.part03 overlay.tar.xz.part04 overlay.tar.xz.part05 overlay.tar.xz.part06 overlay.tar.xz.part07 > overlay.tar.xz
echo '1e47e59d162b25407eeafd08cb2d251a385c84e4a60b56fb16186ac5004f9502  overlay.tar.xz' | sha256sum -c -
tar -tJf overlay.tar.xz >/dev/null
echo 'Verified V6.2 Chemistry overlay is ready for extraction after the V6.1.4 rescue overlay.'
