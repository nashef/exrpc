# Copyright (c) 2014, Nash E. Foster
#
#  This file is part of Exrpc.
#
#  Exrpc is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Exrpc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Exrpc.  If not, see <http://www.gnu.org/licenses/>.
#

thrift:
	mkdir -p srv
	thrift -r --gen py -out srv string_service.thrift

clean:
	rm -rf srv
