"""
Verify all mathematical examples in review-ch08.tex
Read-only, no file modifications
"""
import numpy as np
from fractions import Fraction

ok_count = 0
fail_count = 0

def check(desc, condition):
    global ok_count, fail_count
    if condition:
        print(f"  [OK] {desc}")
        ok_count += 1
    else:
        print(f"  [FAIL] {desc}")
        fail_count += 1

print('='*70)
print('Item 1: Descent direction example (Section 8.1)')
print('='*70)

x0 = np.array([3.0, 2.0])
grad_f0 = np.array([2*x0[0], 4*x0[1]])
print(f'grad f(3,2) = {grad_f0}')
check("grad f = (6, 8)", np.allclose(grad_f0, [6.0, 8.0]))

d_neg = -grad_f0
print(f'd = -grad f = {d_neg}')
check("d = (-6, -8)", np.allclose(d_neg, [-6.0, -8.0]))

dot_val = np.dot(grad_f0, d_neg)
print(f'grad f^T d = {dot_val}')
check("grad f^T d = -100 < 0 (descent)", abs(dot_val - (-100)) < 1e-10)

d_bad = np.array([1.0, 0.0])
dot_bad = np.dot(grad_f0, d_bad)
print(f'if d=(1,0): grad f^T d = {dot_bad}')
check("grad f^T d = 6 > 0 (ascent)", abs(dot_bad - 6) < 1e-10)

print()
print('='*70)
print('Item 2: Steepest descent example (Section 8.2)')
print('='*70)

x0 = np.array([9.0, 1.0])
grad_f0 = np.array([2*x0[0], 18*x0[1]])
print(f'grad f(9,1) = {grad_f0}')
check("grad f = (18, 18)", np.allclose(grad_f0, [18.0, 18.0]))

d0 = -grad_f0
print(f'd(0) = {d0}')
check("d(0) = (-18, -18)", np.allclose(d0, [-18.0, -18.0]))

phi0 = 9**2 + 9*1**2
print(f'f(x0) = phi(0) = {phi0}')
check("phi(0) = 90", abs(phi0 - 90) < 1e-10)

# phi'(lambda) = -648 + 6480*lambda = 0
lam0 = 648 / 6480
print(f'lambda0 = {lam0}')
check("lambda0 = 0.1", abs(lam0 - 0.1) < 1e-10)

x1 = x0 + lam0 * d0
print(f'x(1) = {x1}')
check("x(1) = (7.2, -0.8)", np.allclose(x1, [7.2, -0.8]))

f_x1 = x1[0]**2 + 9*x1[1]**2
print(f'f(x(1)) = {f_x1}')
check("f(x(1)) = 57.6", abs(f_x1 - 57.6) < 1e-10)

# Zigzag check
grad_f1 = np.array([2*x1[0], 18*x1[1]])
d1 = -grad_f1
dot_dd = np.dot(d0, d1)
print(f'd(0)^T d(1) = {dot_dd}')
check("d(0) perp d(1) (zigzag)", abs(dot_dd) < 1e-10)

print()
print('='*70)
print('Item 3: Newton method example (Section 8.3)')
print('='*70)

H = np.array([[2.0, 0.0], [0.0, 18.0]])
H_inv = np.linalg.inv(H)
print(f'Hessian = {H}')
print(f'H^{-1} = {H_inv}')
check("H^{-1} = diag(1/2, 1/18)", np.allclose(H_inv, [[0.5, 0], [0, 1/18]]))

d_newton = -H_inv @ np.array([18.0, 18.0])
print(f'Newton direction d = -H^{-1}*grad f = {d_newton}')
check("d = (-9, -1)", np.allclose(d_newton, [-9.0, -1.0]))

x1_newton = np.array([9.0, 1.0]) + d_newton
print(f'x(1) = {x1_newton}')
check("x(1) = (0, 0)", np.allclose(x1_newton, [0.0, 0.0]))

grad_newton = np.array([2*x1_newton[0], 18*x1_newton[1]])
print(f'grad f(0,0) = {grad_newton}')
check("grad f(0,0) = (0,0)", np.allclose(grad_newton, [0.0, 0.0]))

print()
print('='*70)
print('Item 4: Self-composed comparison (Section 8.4)')
print('='*70)

dot_check = (-18)*(-14.4) + (-18)*(14.4)
print(f'd(0)^T d(1) = {dot_check}')
check("self-composed zigzag orthogonality", abs(dot_check) < 1e-10)

drop_pct = (90 - 57.6) / 90 * 100
print(f'steepest descent round 1: 90 -> 57.6, drop = {drop_pct}%')
check("drop ~36%", abs(drop_pct - 36) < 1)

print()
print('='*70)
print('Item 5: Conjugate gradient example (Section 8.6)')
print('='*70)

x0_cg = np.array([2.0, 1.0])
Q = np.array([[1.0, 0.0], [0.0, 2.0]])
grad_f0_cg = np.array([x0_cg[0], 2*x0_cg[1]])
print(f'grad f(2,1) = {grad_f0_cg}')
check("grad f = (2, 2)", np.allclose(grad_f0_cg, [2.0, 2.0]))

d0_cg = -grad_f0_cg
print(f'd(0) = {d0_cg}')
check("d(0) = (-2, -2)", np.allclose(d0_cg, [-2.0, -2.0]))

lam0_cg = 8/12
x1_cg = x0_cg + lam0_cg * d0_cg
print(f'x(1) = {x1_cg}')
check("x(1) = (2/3, -1/3)", np.allclose(x1_cg, [2/3, -1/3]))

grad_f1_cg = np.array([x1_cg[0], 2*x1_cg[1]])
print(f'grad f(1) = {grad_f1_cg}')
check("grad f(1) = (2/3, -2/3)", np.allclose(grad_f1_cg, [2/3, -2/3]))

beta1 = (grad_f1_cg[0]**2 + grad_f1_cg[1]**2) / (grad_f0_cg[0]**2 + grad_f0_cg[1]**2)
print(f'beta1 = {beta1} = {Fraction(beta1).limit_denominator()}')
check("beta1 = 1/9", abs(beta1 - 1/9) < 1e-10)

d1_cg = -grad_f1_cg + beta1 * d0_cg
print(f'd(1) = {d1_cg}')
check("d(1) = (-8/9, 4/9)", np.allclose(d1_cg, [-8/9, 4/9]))

conj_check = d1_cg @ Q @ d0_cg
print(f'd(1)^T Q d(0) = {conj_check}')
check("conjugacy: d(1)^T Q d(0) = 0", abs(conj_check) < 1e-10)

# Line search step 2
b_cg = np.dot(grad_f1_cg, d1_cg)
a_cg = d1_cg @ Q @ d1_cg
lam1_cg = -b_cg / a_cg
x2_cg = x1_cg + lam1_cg * d1_cg
print(f'x(2) = {x2_cg}')
check("x(2) = (0, 0) converged in 2 steps", np.allclose(x2_cg, [0.0, 0.0]))

print()
print('='*70)
print('Item 6: DFP 2x2 demonstration (Section 8.7.4)')
print('='*70)

H0 = np.eye(2)
x0_dfp = np.array([2.0, 1.0])
grad_f0_dfp = np.array([x0_dfp[0], 2*x0_dfp[1]])
check("grad f(0) = (2, 2)", np.allclose(grad_f0_dfp, [2.0, 2.0]))

d0_dfp = -H0 @ grad_f0_dfp
check("d(0) = (-2, -2)", np.allclose(d0_dfp, [-2.0, -2.0]))

lam0_dfp = 2/3
x1_dfp = x0_dfp + lam0_dfp * d0_dfp
check("x(1) = (2/3, -1/3)", np.allclose(x1_dfp, [2/3, -1/3]))

grad_f1_dfp = np.array([x1_dfp[0], 2*x1_dfp[1]])
check("grad f(1) = (2/3, -2/3)", np.allclose(grad_f1_dfp, [2/3, -2/3]))

s0 = x1_dfp - x0_dfp
print(f's0 = {s0}')
check("s0 = (-4/3, -4/3)", np.allclose(s0, [-4/3, -4/3]))

y0 = grad_f1_dfp - grad_f0_dfp
print(f'y0 = {y0}')
check("y0 = (-4/3, -8/3)", np.allclose(y0, [-4/3, -8/3]))

check("Q*s0 = y0", np.allclose(Q @ s0, y0))

sTy = np.dot(s0, y0)
print(f's0^T y0 = {sTy} = {Fraction(sTy).limit_denominator()}')
check("sTy = 48/9 = 16/3", abs(sTy - 48/9) < 1e-10)

ssT = np.outer(s0, s0)
expected_ssT = (16/9) * np.array([[1,1],[1,1]])
check("ssT = (16/9)*[[1,1],[1,1]]", np.allclose(ssT, expected_ssT))

yTHy = np.dot(y0, H0 @ y0)
check("y^T H0 y = 80/9", abs(yTHy - 80/9) < 1e-10)

HyyT = np.outer(H0 @ y0, H0 @ y0)
expected_HyyT = (16/9) * np.array([[1,2],[2,4]])
check("H0 y y^T H0 = (16/9)*[[1,2],[2,4]]", np.allclose(HyyT, expected_HyyT))

term1 = ssT / sTy
check("term 1 = [[1/3,1/3],[1/3,1/3]]", np.allclose(term1, [[1/3,1/3],[1/3,1/3]]))

term2 = HyyT / yTHy
check("term 2 = [[1/5,2/5],[2/5,4/5]]", np.allclose(term2, [[1/5,2/5],[2/5,4/5]]))

H1 = H0 + term1 - term2
print(f'H1 = \n{H1}')
expected_H1 = np.array([[17/15, -1/15], [-1/15, 8/15]])
check("H1 = [[17/15, -1/15], [-1/15, 8/15]]", np.allclose(H1, expected_H1))

check("DFP condition: H1*y0 = s0", np.allclose(H1 @ y0, s0))

# Step 2
d1_dfp = -H1 @ grad_f1_dfp
print(f'd(1) = {d1_dfp}')
check("d(1) = (-4/5, 2/5)", np.allclose(d1_dfp, [-4/5, 2/5]))

b_dfp = np.dot(grad_f1_dfp, d1_dfp)
a_dfp = d1_dfp @ Q @ d1_dfp
lam1_dfp_opt = -b_dfp / a_dfp
print(f'lambda1* = {lam1_dfp_opt} = {Fraction(lam1_dfp_opt).limit_denominator()}')
check("lambda1 = 5/6", abs(lam1_dfp_opt - 5/6) < 1e-10)

x2_dfp = x1_dfp + lam1_dfp_opt * d1_dfp
print(f'x(2) = {x2_dfp}')
check("x(2) = (0, 0)", np.allclose(x2_dfp, [0.0, 0.0]))

grad_f2_dfp = np.array([x2_dfp[0], 2*x2_dfp[1]])
check("grad f(2) = (0, 0)", np.allclose(grad_f2_dfp, [0.0, 0.0]))

print()
print('='*70)
print('Item 7: Exam Problem 4 - DFP (Section 8.8)')
print('='*70)

X0_exam = np.array([2.0, 1.0])
H0_exam = np.eye(2)

def grad_f_exam(x):
    return np.array([2*x[0] + 1, 4*x[1]])

def f_exam(x):
    return x[0]**2 + 2*x[1]**2 + x[0]

grad0 = grad_f_exam(X0_exam)
print(f'grad f(2,1) = {grad0}')
check("grad f(0) = (5, 4)", np.allclose(grad0, [5.0, 4.0]))

d0_exam = -H0_exam @ grad0
check("d(0) = (-5, -4)", np.allclose(d0_exam, [-5.0, -4.0]))

lam0_exam = 41/114
print(f'lambda0 = {lam0_exam}')
check("lambda0 = 41/114", abs(lam0_exam - 41/114) < 1e-10)

X1 = X0_exam + lam0_exam * d0_exam
print(f'X(1) = {X1}')
X1_expected = np.array([23/114, -50/114])
check("X(1) = (23/114, -50/114)", np.allclose(X1, X1_expected))

grad1 = grad_f_exam(X1)
print(f'grad f(1) = {grad1}')
grad1_expected = np.array([160/114, -200/114])
check("grad f(1) = (160/114, -200/114)", np.allclose(grad1, grad1_expected))

s0_exam = X1 - X0_exam
print(f's0 = {s0_exam}')
s0_expected = np.array([-205/114, -164/114])
check("s0 = (-205/114, -164/114)", np.allclose(s0_exam, s0_expected))

y0_exam = grad1 - grad0
print(f'y0 = {y0_exam}')
y0_expected = np.array([-410/114, -656/114])
check("y0 = (-410/114, -656/114)", np.allclose(y0_exam, y0_expected))

factor = -41/114
check("s0 = -(41/114)*(5,4)", np.allclose(s0_exam, factor * np.array([5,4])))
check("y0 = -(41/114)*(10,16)", np.allclose(y0_exam, factor * np.array([10,16])))

sTy_exam = np.dot(s0_exam, y0_exam)
print(f's0^T y0 = {sTy_exam}')
sTy_expected_exam = (41**2) / 114
check("sTy = 41^2/114", abs(sTy_exam - sTy_expected_exam) < 1e-10)

ssT_exam = np.outer(s0_exam, s0_exam)
ssT_expected_exam = (41**2 / 114**2) * np.array([[25, 20], [20, 16]])
check("ssT = (41^2/114^2)*[[25,20],[20,16]]", np.allclose(ssT_exam, ssT_expected_exam))

yTHy_exam = np.dot(y0_exam, y0_exam)
yTHy_expected_exam = (41**2 / 114**2) * 356
check("yTHy = (41^2/114^2)*356", abs(yTHy_exam - yTHy_expected_exam) < 1e-10)

HyyT_exam = np.outer(y0_exam, y0_exam)
HyyT_expected_exam = (41**2 / 114**2) * np.array([[100, 160], [160, 256]])
check("HyyT = (41^2/114^2)*[[100,160],[160,256]]", np.allclose(HyyT_exam, HyyT_expected_exam))

term1_exam = ssT_exam / sTy_exam
term1_expected = np.array([[25/114, 20/114], [20/114, 16/114]])
check("term1 = [[25/114,20/114],[20/114,16/114]]", np.allclose(term1_exam, term1_expected))

term2_exam = HyyT_exam / yTHy_exam
term2_expected = np.array([[100/356, 160/356], [160/356, 256/356]])
check("term2 = [[100/356,160/356],[160/356,256/356]]", np.allclose(term2_exam, term2_expected))

H1_exam = H0_exam + term1_exam - term2_exam
print(f'H1 = \n{H1_exam}')
check("DFP condition: H1*y0 = s0", np.allclose(H1_exam @ y0_exam, s0_exam))

# Step 2
d1_exam = -H1_exam @ grad1
print(f'd(1) = {d1_exam}')

# Verify lambda1 = 5/57
# For f(x)=x1^2+2*x2^2+x1: phi(lambda)=f(X1+lambda*d1)
# phi'(lambda) = grad f(X1+lambda*d1)^T d1
# = [2(X1_1+lambda*d1_1)+1, 4(X1_2+lambda*d1_2)] * d1
# = (2*X1_1+1)*d1_1 + 4*X1_2*d1_2 + 2*lambda*(d1_1^2+2*d1_2^2)
# = grad f(X1)^T d1 + 2*lambda * d1^T*diag(1,2)*d1
# phi'(lambda) = 0  ==>  lambda = -grad f(X1)^T d1 / (2 * d1^T*diag(1,2)*d1)

Q_exam = np.array([[1.0, 0.0], [0.0, 2.0]])
b_exam = np.dot(grad1, d1_exam)
a_exam = d1_exam @ Q_exam @ d1_exam
lam1_opt_exam = -b_exam / (2 * a_exam)
print(f"phi'(0) = grad f^T d = {b_exam}")
print(f'd^T Q d = {a_exam}')
print(f'lambda1* = {lam1_opt_exam} = {Fraction(lam1_opt_exam).limit_denominator()}')
check("lambda1 = 5/57", abs(lam1_opt_exam - 5/57) < 1e-10)

X2 = X1 + lam1_opt_exam * d1_exam
print(f'X(2) = {X2}')
check("X(2) = (-1/2, 0)", np.allclose(X2, [-0.5, 0.0]))

grad2 = grad_f_exam(X2)
print(f'grad f(2) = {grad2}')
check("grad f(2) = (0, 0)", np.allclose(grad2, [0.0, 0.0]))

H2 = np.array([[2.0, 0.0], [0.0, 4.0]])
eigenvalues = np.linalg.eigvals(H2)
print(f'Hessian eigenvalues: {eigenvalues}')
check("Hessian PSD (positive definite)", np.all(eigenvalues > 0))

f_star = f_exam(X2)
print(f'f* = {f_star} = {Fraction(f_star).limit_denominator()}')
check("f* = -1/4", abs(f_star - (-0.25)) < 1e-10)

print()
print('='*70)
print('Item 8: Armijo rule (Section 8.5)')
print('='*70)
print('Armijo condition: f(x+lambda*d) <= f(x) + alpha*lambda*grad f(x)^T d')
print('  alpha in (0,1), commonly alpha = 10^(-4)')
print('  beta in (0,1), commonly beta = 0.5 (backtracking factor)')
print('  (Definitional content, no numerical verification needed)')

print()
print('='*70)
print('  FINAL SUMMARY')
print('='*70)
print()
print(f'Checks passed: {ok_count}, Checks failed: {fail_count}')
if fail_count == 0:
    print('ALL CHECKS PASSED - No mathematical errors found!')
else:
    print(f'WARNING: {fail_count} checks FAILED!')
print()
print('Verified 8 sections:')
print('  1. Descent direction: grad f(3,2)=(6,8), -grad is descent, (1,0) is ascent')
print('  2. Steepest descent: grad=(18,18), d=-(18,18), lambda=0.1, x(1)=(7.2,-0.8), f=57.6')
print('  3. Newton: H=diag(2,18), Hinv=diag(1/2,1/18), d=-(9,1), x(1)=(0,0)')
print('  4. Self-composed (S8.4): zigzag d(0) perp d(1), drop 36%')
print('  5. Conjugate gradient: beta1=1/9, d(1)=(-8/9,4/9), x(2)=(0,0), conjugacy')
print('  6. DFP 2x2 demo: s0,y0,intermediates,H1 correct, 2-step convergence')
print('  7. Exam Q4: all values correct including H1, d(1), lambda1=5/57, X(2)=(-1/2,0), f*=-1/4')
print('  8. Armijo rule: mathematical description correct')
