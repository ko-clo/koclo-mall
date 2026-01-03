export interface Address {
	id: string;
	name: string; // 배송지명 (예: 집, 회사)
	recipient: string;
	phone: string;
	postal_code: string;
	address: string;
	address_detail: string;
	is_default: boolean;
	created_at: string;
}

// Mock 배송지 데이터
export const mockAddresses: Address[] = [
	{
		id: 'addr-1',
		name: '집',
		recipient: '홍길동',
		phone: '010-1234-5678',
		postal_code: '06000',
		address: '서울특별시 강남구 테헤란로 123',
		address_detail: '456호',
		is_default: true,
		created_at: '2024-12-01T10:00:00Z'
	},
	{
		id: 'addr-2',
		name: '회사',
		recipient: '홍길동',
		phone: '010-1234-5678',
		postal_code: '12345',
		address: '경기도 성남시 분당구 판교역로 235',
		address_detail: '101동 202호',
		is_default: false,
		created_at: '2024-12-15T14:30:00Z'
	},
	{
		id: 'addr-3',
		name: '부모님 댁',
		recipient: '김영희',
		phone: '010-9876-5432',
		postal_code: '03000',
		address: '서울특별시 종로구 세종대로 209',
		address_detail: '',
		is_default: false,
		created_at: '2024-12-20T09:15:00Z'
	}
];

export function getAddresses(): Address[] {
	return [...mockAddresses].sort((a, b) => {
		// 기본 배송지가 맨 위로
		if (a.is_default) return -1;
		if (b.is_default) return 1;
		// 나머지는 최신순
		return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
	});
}

export function getAddressById(id: string): Address | undefined {
	return mockAddresses.find(addr => addr.id === id);
}

export function getDefaultAddress(): Address | undefined {
	return mockAddresses.find(addr => addr.is_default);
}

export function formatPhoneNumber(phone: string): string {
	// 010-1234-5678 형식으로 포맷팅
	const cleaned = phone.replace(/\D/g, '');
	if (cleaned.length === 11) {
		return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 7)}-${cleaned.slice(7)}`;
	}
	return phone;
}

// 배송지 등록
export async function addAddress(
	address: Omit<Address, 'id' | 'created_at'>
): Promise<Address> {
	// 최대 10개 제한
	if (mockAddresses.length >= 10) {
		throw new Error('최대 10개까지 배송지를 등록할 수 있습니다.');
	}

	// API 호출 시뮬레이션 (0.5초 대기)
	await new Promise(resolve => setTimeout(resolve, 500));

	// 첫 배송지인 경우 자동으로 기본 배송지로 설정
	const isFirst = mockAddresses.length === 0;
	const isDefault = isFirst ? true : address.is_default;

	// 기본 배송지로 설정하는 경우 기존 기본 배송지 해제
	if (isDefault) {
		mockAddresses.forEach(addr => {
			addr.is_default = false;
		});
	}

	const newAddress: Address = {
		id: `addr-${Date.now()}`,
		...address,
		is_default: isDefault,
		created_at: new Date().toISOString()
	};

	mockAddresses.push(newAddress);

	return newAddress;
}

// 배송지 수정
export async function updateAddress(
	id: string,
	updates: Partial<Omit<Address, 'id' | 'created_at'>>
): Promise<Address> {
	const index = mockAddresses.findIndex(addr => addr.id === id);

	if (index === -1) {
		throw new Error('배송지를 찾을 수 없습니다.');
	}

	// API 호출 시뮬레이션 (0.5초 대기)
	await new Promise(resolve => setTimeout(resolve, 500));

	// 기본 배송지로 설정하는 경우 기존 기본 배송지 해제
	if (updates.is_default) {
		mockAddresses.forEach(addr => {
			addr.is_default = false;
		});
	}

	// 배송지 업데이트
	mockAddresses[index] = {
		...mockAddresses[index],
		...updates
	};

	return mockAddresses[index];
}

// 기본 배송지 설정
export async function setDefaultAddress(id: string): Promise<Address> {
	const index = mockAddresses.findIndex(addr => addr.id === id);

	if (index === -1) {
		throw new Error('배송지를 찾을 수 없습니다.');
	}

	// 이미 기본 배송지인 경우
	if (mockAddresses[index].is_default) {
		return mockAddresses[index];
	}

	// API 호출 시뮬레이션 (0.5초 대기)
	await new Promise(resolve => setTimeout(resolve, 500));

	// 기존 기본 배송지 해제
	mockAddresses.forEach(addr => {
		addr.is_default = false;
	});

	// 새 기본 배송지 설정
	mockAddresses[index].is_default = true;

	return mockAddresses[index];
}

// 배송지 삭제
export async function deleteAddress(id: string): Promise<boolean> {
	const index = mockAddresses.findIndex(addr => addr.id === id);

	if (index === -1) {
		throw new Error('배송지를 찾을 수 없습니다.');
	}

	const address = mockAddresses[index];

	// 기본 배송지는 삭제 불가
	if (address.is_default) {
		throw new Error('기본 배송지는 삭제할 수 없습니다. 다른 배송지를 기본으로 설정 후 삭제해주세요.');
	}

	// API 호출 시뮬레이션 (0.5초 대기)
	await new Promise(resolve => setTimeout(resolve, 500));

	// 배송지 삭제
	mockAddresses.splice(index, 1);

	return true;
}
