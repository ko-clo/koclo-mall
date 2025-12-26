import { z } from 'zod';

export const loginSchema = z.object({
	email: z.string().email('올바른 이메일 형식이 아닙니다'),
	password: z.string().min(1, '비밀번호를 입력해주세요')
});

export const signupSchema = z
	.object({
		email: z.string().email('올바른 이메일 형식이 아닙니다'),
		password: z
			.string()
			.min(8, '비밀번호는 8자 이상이어야 합니다')
			.max(20, '비밀번호는 20자 이하여야 합니다')
			.regex(
				/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])/,
				'영문, 숫자, 특수문자를 모두 포함해야 합니다'
			),
		passwordConfirm: z.string(),
		name: z
			.string()
			.min(2, '이름은 2자 이상이어야 합니다')
			.max(50, '이름은 50자 이하여야 합니다'),
		phone: z.string().optional(),
		agreements: z.object({
			terms: z.literal(true, { message: '이용약관에 동의해주세요' }),
			privacy: z.literal(true, { message: '개인정보처리방침에 동의해주세요' }),
			marketing: z.boolean().optional()
		})
	})
	.refine((data) => data.password === data.passwordConfirm, {
		message: '비밀번호가 일치하지 않습니다',
		path: ['passwordConfirm']
	});

export type LoginInput = z.infer<typeof loginSchema>;
export type SignupInput = z.infer<typeof signupSchema>;
