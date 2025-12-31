export interface Product {
	id: string;
	name: string;
	slug: string;
	thumbnail_url: string;
	images: { id: string; url: string; is_thumbnail: boolean; sort_order: number }[];
	original_price: number;
	display_price: number;
	discount_rate: number;
	short_description: string;
	description: string;
	is_sold_out: boolean;
	is_new: boolean;
	is_deleted: boolean;
	deleted_at?: string;
	category: { id: string; name: string; slug: string };
	options: ProductOption[];
}

export interface ProductOption {
	id: string;
	sku: string;
	color: string;
	size: string;
	stock_quantity: number;
	additional_price: number;
}

export const mockProducts: Product[] = [
	{
		id: '1',
		name: '오버핏 캐시미어 니트',
		slug: 'overfit-cashmere-knit',
		thumbnail_url: 'https://picsum.photos/seed/knit1/400/533',
		images: [
			{ id: '1-1', url: 'https://picsum.photos/seed/knit1/800/1066', is_thumbnail: true, sort_order: 1 },
			{ id: '1-2', url: 'https://picsum.photos/seed/knit1-2/800/1066', is_thumbnail: false, sort_order: 2 },
			{ id: '1-3', url: 'https://picsum.photos/seed/knit1-3/800/1066', is_thumbnail: false, sort_order: 3 }
		],
		original_price: 89000,
		display_price: 62000,
		discount_rate: 30,
		short_description: '부드러운 캐시미어 블렌드 니트',
		description: '<p>프리미엄 캐시미어 블렌드 소재로 제작된 오버핏 니트입니다.</p>',
		is_sold_out: false,
		is_new: true,
		is_deleted: false,
		category: { id: 'cat-1', name: '니트', slug: 'top/knit' },
		options: [
			{ id: 'opt-1-1', sku: 'KNC-BLK-S', color: 'Black', size: 'S', stock_quantity: 10, additional_price: 0 },
			{ id: 'opt-1-2', sku: 'KNC-BLK-M', color: 'Black', size: 'M', stock_quantity: 15, additional_price: 0 },
			{ id: 'opt-1-3', sku: 'KNC-BLK-L', color: 'Black', size: 'L', stock_quantity: 8, additional_price: 0 },
			{ id: 'opt-1-4', sku: 'KNC-IVR-S', color: 'Ivory', size: 'S', stock_quantity: 12, additional_price: 0 },
			{ id: 'opt-1-5', sku: 'KNC-IVR-M', color: 'Ivory', size: 'M', stock_quantity: 20, additional_price: 0 },
			{ id: 'opt-1-6', sku: 'KNC-IVR-L', color: 'Ivory', size: 'L', stock_quantity: 5, additional_price: 0 }
		]
	},
	{
		id: '2',
		name: '울 블렌드 롱 코트',
		slug: 'wool-blend-long-coat',
		thumbnail_url: 'https://picsum.photos/seed/coat1/400/533',
		images: [
			{ id: '2-1', url: 'https://picsum.photos/seed/coat1/800/1066', is_thumbnail: true, sort_order: 1 },
			{ id: '2-2', url: 'https://picsum.photos/seed/coat1-2/800/1066', is_thumbnail: false, sort_order: 2 }
		],
		original_price: 189000,
		display_price: 129000,
		discount_rate: 32,
		short_description: '클래식한 디자인의 울 블렌드 코트',
		description: '<p>고급 울 블렌드 소재의 클래식 롱 코트입니다.</p>',
		is_sold_out: false,
		is_new: false,
		is_deleted: false,
		category: { id: 'cat-2', name: '코트', slug: 'outer/coat' },
		options: [
			{ id: 'opt-2-1', sku: 'WLC-BLK-M', color: 'Black', size: 'M', stock_quantity: 5, additional_price: 0 },
			{ id: 'opt-2-2', sku: 'WLC-BLK-L', color: 'Black', size: 'L', stock_quantity: 3, additional_price: 0 },
			{ id: 'opt-2-3', sku: 'WLC-CAM-M', color: 'Camel', size: 'M', stock_quantity: 7, additional_price: 0 },
			{ id: 'opt-2-4', sku: 'WLC-CAM-L', color: 'Camel', size: 'L', stock_quantity: 4, additional_price: 0 }
		]
	},
	{
		id: '3',
		name: '와이드 데님 팬츠',
		slug: 'wide-denim-pants',
		thumbnail_url: 'https://picsum.photos/seed/denim1/400/533',
		images: [
			{ id: '3-1', url: 'https://picsum.photos/seed/denim1/800/1066', is_thumbnail: true, sort_order: 1 }
		],
		original_price: 69000,
		display_price: 49000,
		discount_rate: 29,
		short_description: '트렌디한 와이드 핏 데님',
		description: '<p>편안한 착용감의 와이드 핏 데님 팬츠입니다.</p>',
		is_sold_out: false,
		is_new: true,
		is_deleted: false,
		category: { id: 'cat-3', name: '팬츠', slug: 'bottom/pants' },
		options: [
			{ id: 'opt-3-1', sku: 'WDP-BLU-S', color: 'Blue', size: 'S', stock_quantity: 20, additional_price: 0 },
			{ id: 'opt-3-2', sku: 'WDP-BLU-M', color: 'Blue', size: 'M', stock_quantity: 25, additional_price: 0 },
			{ id: 'opt-3-3', sku: 'WDP-BLU-L', color: 'Blue', size: 'L', stock_quantity: 15, additional_price: 0 }
		]
	},
	{
		id: '4',
		name: '크롭 패딩 자켓',
		slug: 'crop-padding-jacket',
		thumbnail_url: 'https://picsum.photos/seed/padding1/400/533',
		images: [
			{ id: '4-1', url: 'https://picsum.photos/seed/padding1/800/1066', is_thumbnail: true, sort_order: 1 },
			{ id: '4-2', url: 'https://picsum.photos/seed/padding1-2/800/1066', is_thumbnail: false, sort_order: 2 }
		],
		original_price: 129000,
		display_price: 89000,
		discount_rate: 31,
		short_description: '따뜻한 크롭 기장 패딩',
		description: '<p>가볍고 따뜻한 크롭 기장의 패딩 자켓입니다.</p>',
		is_sold_out: false,
		is_new: false,
		is_deleted: false,
		category: { id: 'cat-4', name: '패딩', slug: 'outer/padding' },
		options: [
			{ id: 'opt-4-1', sku: 'CPJ-BLK-S', color: 'Black', size: 'S', stock_quantity: 8, additional_price: 0 },
			{ id: 'opt-4-2', sku: 'CPJ-BLK-M', color: 'Black', size: 'M', stock_quantity: 12, additional_price: 0 },
			{ id: 'opt-4-3', sku: 'CPJ-WHT-S', color: 'White', size: 'S', stock_quantity: 6, additional_price: 0 },
			{ id: 'opt-4-4', sku: 'CPJ-WHT-M', color: 'White', size: 'M', stock_quantity: 10, additional_price: 0 }
		]
	},
	{
		id: '5',
		name: '스트라이프 오버핏 셔츠',
		slug: 'stripe-overfit-shirt',
		thumbnail_url: 'https://picsum.photos/seed/shirt1/400/533',
		images: [
			{ id: '5-1', url: 'https://picsum.photos/seed/shirt1/800/1066', is_thumbnail: true, sort_order: 1 }
		],
		original_price: 59000,
		display_price: 59000,
		discount_rate: 0,
		short_description: '클래식 스트라이프 패턴 셔츠',
		description: '<p>깔끔한 스트라이프 패턴의 오버핏 셔츠입니다.</p>',
		is_sold_out: false,
		is_new: true,
		is_deleted: false,
		category: { id: 'cat-5', name: '셔츠', slug: 'top/shirt' },
		options: [
			{ id: 'opt-5-1', sku: 'SOS-BLU-M', color: 'Blue', size: 'M', stock_quantity: 15, additional_price: 0 },
			{ id: 'opt-5-2', sku: 'SOS-BLU-L', color: 'Blue', size: 'L', stock_quantity: 18, additional_price: 0 }
		]
	},
	{
		id: '6',
		name: '플리스 집업 자켓',
		slug: 'fleece-zipup-jacket',
		thumbnail_url: 'https://picsum.photos/seed/fleece1/400/533',
		images: [
			{ id: '6-1', url: 'https://picsum.photos/seed/fleece1/800/1066', is_thumbnail: true, sort_order: 1 }
		],
		original_price: 79000,
		display_price: 55000,
		discount_rate: 30,
		short_description: '포근한 플리스 소재 자켓',
		description: '<p>부드러운 플리스 소재의 집업 자켓입니다.</p>',
		is_sold_out: true,
		is_new: false,
		is_deleted: true,
		deleted_at: '2025-12-28T10:00:00Z',
		category: { id: 'cat-6', name: '자켓', slug: 'outer/jacket' },
		options: [
			{ id: 'opt-6-1', sku: 'FZJ-CRM-M', color: 'Cream', size: 'M', stock_quantity: 0, additional_price: 0 },
			{ id: 'opt-6-2', sku: 'FZJ-CRM-L', color: 'Cream', size: 'L', stock_quantity: 0, additional_price: 0 }
		]
	},
	{
		id: '7',
		name: '울 머플러',
		slug: 'wool-muffler',
		thumbnail_url: 'https://picsum.photos/seed/muffler1/400/533',
		images: [
			{ id: '7-1', url: 'https://picsum.photos/seed/muffler1/800/1066', is_thumbnail: true, sort_order: 1 }
		],
		original_price: 39000,
		display_price: 29000,
		discount_rate: 26,
		short_description: '따뜻한 울 머플러',
		description: '<p>고급 울 소재의 머플러입니다.</p>',
		is_sold_out: false,
		is_new: false,
		is_deleted: false,
		category: { id: 'cat-7', name: '머플러', slug: 'acc/muffler' },
		options: [
			{ id: 'opt-7-1', sku: 'WMF-GRY-F', color: 'Gray', size: 'Free', stock_quantity: 30, additional_price: 0 },
			{ id: 'opt-7-2', sku: 'WMF-BLK-F', color: 'Black', size: 'Free', stock_quantity: 25, additional_price: 0 }
		]
	},
	{
		id: '8',
		name: '레더 토트백',
		slug: 'leather-tote-bag',
		thumbnail_url: 'https://picsum.photos/seed/bag1/400/533',
		images: [
			{ id: '8-1', url: 'https://picsum.photos/seed/bag1/800/1066', is_thumbnail: true, sort_order: 1 }
		],
		original_price: 99000,
		display_price: 69000,
		discount_rate: 30,
		short_description: '데일리 레더 토트백',
		description: '<p>실용적인 사이즈의 레더 토트백입니다.</p>',
		is_sold_out: false,
		is_new: true,
		is_deleted: false,
		category: { id: 'cat-8', name: '가방', slug: 'acc/bag' },
		options: [
			{ id: 'opt-8-1', sku: 'LTB-BLK-F', color: 'Black', size: 'Free', stock_quantity: 20, additional_price: 0 },
			{ id: 'opt-8-2', sku: 'LTB-BRN-F', color: 'Brown', size: 'Free', stock_quantity: 15, additional_price: 0 }
		]
	}
];

export const categories = [
	{ id: 'cat-outer', name: '아우터', slug: 'outer', children: [
		{ id: 'cat-coat', name: '코트', slug: 'outer/coat' },
		{ id: 'cat-jacket', name: '자켓', slug: 'outer/jacket' },
		{ id: 'cat-padding', name: '패딩', slug: 'outer/padding' }
	]},
	{ id: 'cat-top', name: '상의', slug: 'top', children: [
		{ id: 'cat-knit', name: '니트', slug: 'top/knit' },
		{ id: 'cat-shirt', name: '셔츠', slug: 'top/shirt' }
	]},
	{ id: 'cat-bottom', name: '하의', slug: 'bottom', children: [
		{ id: 'cat-pants', name: '팬츠', slug: 'bottom/pants' }
	]},
	{ id: 'cat-acc', name: '악세서리', slug: 'acc', children: [
		{ id: 'cat-muffler', name: '머플러', slug: 'acc/muffler' },
		{ id: 'cat-bag', name: '가방', slug: 'acc/bag' }
	]}
];

export function formatPrice(price: number): string {
	return price.toLocaleString('ko-KR') + '원';
}

export function getProductBySlug(slug: string): Product | undefined {
	return mockProducts.find(p => p.slug === slug);
}

export function getProductByOptionId(optionId: string): { product: Product; option: ProductOption } | undefined {
	for (const product of mockProducts) {
		const option = product.options.find(o => o.id === optionId);
		if (option) {
			return { product, option };
		}
	}
	return undefined;
}
