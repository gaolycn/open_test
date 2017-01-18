#!/bin/bash

# 单元测试
# ./runtest.sh test_coupon_use.py:TestCouponUse.test_coupon_code_invalid
if [[ $# -eq 1 ]]; then
     /home/qfpay/python/bin/nosetests -v $1
else
	 /home/qfpay/python/bin/nosetests -v -e qfcommon -w ./
fi
