import { describe, it, expect } from 'vitest';
import { loginSchema, signupSchema } from './auth';

describe('loginSchema', () => {
	it('유효한 로그인 데이터를 통과시킨다', () => {
		const validData = {
			email: 'test@example.com',
			password: 'password123'
		};
		const result = loginSchema.safeParse(validData);
		expect(result.success).toBe(true);
	});

	it('잘못된 이메일 형식을 거부한다', () => {
		const invalidData = {
			email: 'invalid-email',
			password: 'password123'
		};
		const result = loginSchema.safeParse(invalidData);
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('올바른 이메일 형식이 아닙니다');
		}
	});

	it('빈 비밀번호를 거부한다', () => {
		const invalidData = {
			email: 'test@example.com',
			password: ''
		};
		const result = loginSchema.safeParse(invalidData);
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('비밀번호를 입력해주세요');
		}
	});
});

describe('signupSchema', () => {
	const validData = {
		email: 'test@example.com',
		password: 'Test123!@#',
		passwordConfirm: 'Test123!@#',
		name: '홍길동',
		phone: '010-1234-5678',
		agreements: {
			terms: true as const,
			privacy: true as const,
			marketing: false
		}
	};

	it('유효한 회원가입 데이터를 통과시킨다', () => {
		const result = signupSchema.safeParse(validData);
		expect(result.success).toBe(true);
	});

	it('8자 미만 비밀번호를 거부한다', () => {
		const result = signupSchema.safeParse({
			...validData,
			password: 'Test1!',
			passwordConfirm: 'Test1!'
		});
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('비밀번호는 8자 이상이어야 합니다');
		}
	});

	it('20자 초과 비밀번호를 거부한다', () => {
		const longPassword = 'Test123!@#abcdefghijk';
		const result = signupSchema.safeParse({
			...validData,
			password: longPassword,
			passwordConfirm: longPassword
		});
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('비밀번호는 20자 이하여야 합니다');
		}
	});

	it('특수문자 없는 비밀번호를 거부한다', () => {
		const result = signupSchema.safeParse({
			...validData,
			password: 'Test12345',
			passwordConfirm: 'Test12345'
		});
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('영문, 숫자, 특수문자를 모두 포함해야 합니다');
		}
	});

	it('숫자 없는 비밀번호를 거부한다', () => {
		const result = signupSchema.safeParse({
			...validData,
			password: 'TestTest!@#',
			passwordConfirm: 'TestTest!@#'
		});
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('영문, 숫자, 특수문자를 모두 포함해야 합니다');
		}
	});

	it('비밀번호 불일치를 거부한다', () => {
		const result = signupSchema.safeParse({
			...validData,
			passwordConfirm: 'DifferentPass1!'
		});
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('비밀번호가 일치하지 않습니다');
		}
	});

	it('2자 미만 이름을 거부한다', () => {
		const result = signupSchema.safeParse({
			...validData,
			name: '김'
		});
		expect(result.success).toBe(false);
		if (!result.success) {
			expect(result.error.errors[0].message).toBe('이름은 2자 이상이어야 합니다');
		}
	});

	it('이용약관 미동의를 거부한다', () => {
		const result = signupSchema.safeParse({
			...validData,
			agreements: {
				terms: false,
				privacy: true,
				marketing: false
			}
		});
		expect(result.success).toBe(false);
	});

	it('개인정보처리방침 미동의를 거부한다', () => {
		const result = signupSchema.safeParse({
			...validData,
			agreements: {
				terms: true,
				privacy: false,
				marketing: false
			}
		});
		expect(result.success).toBe(false);
	});

	it('마케팅 동의는 선택사항이다', () => {
		const result = signupSchema.safeParse({
			...validData,
			agreements: {
				terms: true as const,
				privacy: true as const,
				marketing: undefined
			}
		});
		expect(result.success).toBe(true);
	});
});
