# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from cornice import Service

import bodhi.security
import bodhi.services.errors


csrf = Service(name='csrf', path='/csrf', description='CSRF Token',
               # XXX - even though this is really a read-only endpoint,
               # we're going to **mark** it as read-write to CORS so
               # that somebody's exploited browser can't make a cross-site
               # request here to steal the CSRF token and escalate damage.
               cors_origins=bodhi.security.cors_origins_rw)


@csrf.get(accept="text/html", renderer="string",
          error_handler=bodhi.services.errors.html_handler)
def get_csrf_token_html(request):
    return request.session.get_csrf_token()


@csrf.get(accept=("application/json", "text/json"), renderer="json",
          error_handler=bodhi.services.errors.json_handler)
def get_csrf_token_json(request):
    return dict(csrf_token=request.session.get_csrf_token())
