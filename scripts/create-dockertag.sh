#!/bin/bash

#  -------------------------------------------------------------------------
#  Copyright (C) 2023 Violin Yanev
#  -------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#  -------------------------------------------------------------------------

set -e

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "$SCRIPT_DIR"

# write full git commit hash of last change on 'image' folder to stdout
echo -n $(git log --pretty=format:'%H' -n 1 "../image")
