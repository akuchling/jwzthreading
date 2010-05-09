
cov:
	coverage run test/test_jwz.py
	coverage annotate -d /tmp/ jwzthreading.py
