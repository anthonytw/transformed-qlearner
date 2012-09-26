Q-Learning using State and Action Space Reduction Transformations
==============================================================================

Version 1.0  
By Anthony Wertz  
awertz@knights.ucf.edu  

0. Description
------------------------------------------------------------------------------

(Abstract taken from paper "report.pdf" in repository.)

Without using modified methods, the vanilla Q-learning algorithm is not capable
of handling policy construction for even simple problems as soon as the state
space becomes too large. This paper introduces a method of Q-learning policy
generation for large state spaces and dynamic environments by proposing a
simple state space reduction transformation model. The algorithm is based on
the unmodified Q-learning implementation but designed such that it can seamlessly
benefit from many already existing Q-learning improvements.

1. LICENSE
------------------------------------------------------------------------------

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
