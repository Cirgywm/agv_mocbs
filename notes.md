# Algorithm Trial

---
## Notes:

### Algorithm's Solution Validation
bagaimana validasi untuk mengetahui bahwa solusi akhir yang diberikan oleh algoritma mo-cbs
adalah solusi terbaik.
- apakah harus print semua iterasi path findingnya dan bandingkan semua costnya
- apakah ukur dari waktu eksekusi, tapi mau dibandingkan kemana? soalnya denah/peta selalu sama
- atau ada metode validasi lain?

### Algorithm's Expansion Constraints
apakah boleh untuk iterasi algoritma dibatasi?

### NAMOA*
#### Pareto Optimal
kadang-kadang bisa langsung ketemu nilainya dengan waktu eksekusi yang cepat. 
Namun, terkadang bisa sangat lama untuk menemukan nilai pareto optimalnya. 
Hal ini karena algoritma selalu menemukan 

---
## Unsolved Problems
### Collision Detection
function buat deteksi tabrakan masih belum bener. Node memang gaada di vertex yang sama 
tapi dia nabrak secara pathing.

### Solution not Found
kadang bisa solution gak ketemu-temu, mungkin bisa nemu tapi computanional costnya besar. 
untuk yang NAMOA\* approximation dan hybrid masih belum bisa ketemu solutionnya (need more investigation).

---

## General Class Docs:
1. grid map
   - grid.py
2. low level search
   - heuristics.py
   - namoa_star_optim.py (for ***pareto_optimal*** approach)
   - namoa_star_approx.py (for ***epsilon approximation*** approach)
   - namoa_star_hybrid.py (for ***hybrid*** approach)
3. high level search
   - mocbs_node.py
   - mocbs.py (edit low level search module here)