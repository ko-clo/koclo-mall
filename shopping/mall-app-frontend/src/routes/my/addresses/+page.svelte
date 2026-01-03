<script lang="ts">
	import { getAddresses, deleteAddress, type Address } from '$lib/data/addresses';
	import { toastStore } from '$lib/stores/toast';

	let addresses = $state<Address[]>(getAddresses());
	let deletingId = $state<string | null>(null);

	async function handleDelete(id: string) {
		if (!confirm('이 배송지를 삭제하시겠습니까?')) return;

		try {
			deletingId = id;
			await deleteAddress(id);
			addresses = getAddresses();
			toastStore.success('배송지가 삭제되었습니다.');
		} catch (error) {
			toastStore.error(error instanceof Error ? error.message : '배송지 삭제에 실패했습니다.');
		} finally {
			deletingId = null;
		}
	}
</script>

<svelte:head>
	<title>배송지 관리 | ko&clo</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
	<div class="flex items-center justify-between mb-6">
		<h1 class="text-2xl font-bold">배송지 관리</h1>
		<a
			href="/my/addresses/new"
			class="btn-primary text-sm px-4 py-2"
		>
			새 배송지 추가
		</a>
	</div>

	{#if addresses.length === 0}
		<div class="text-center py-20 border rounded-lg">
			<svg
				class="mx-auto h-16 w-16 text-gray-300 mb-4"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="1.5"
					d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
				/>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="1.5"
					d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
				/>
			</svg>
			<p class="text-gray-500 text-lg mb-4">등록된 배송지가 없습니다.</p>
			<a href="/my/addresses/new" class="btn-primary inline-block">배송지 추가하기</a>
		</div>
	{:else}
		<div class="space-y-4">
			{#each addresses as address}
				<div class="border rounded-lg p-6 hover:shadow-md transition-shadow">
					<div class="flex items-start justify-between mb-4">
						<div class="flex items-center gap-2">
							<h3 class="font-bold text-lg">{address.name}</h3>
							{#if address.is_default}
								<span class="px-2 py-1 bg-black text-white text-xs rounded">기본배송지</span>
							{/if}
						</div>
						<div class="flex gap-2">
							<a
								href="/my/addresses/{address.id}/edit"
								class="text-sm text-gray-600 hover:text-black"
							>
								수정
							</a>
							{#if !address.is_default}
								<button
									type="button"
									class="text-sm text-red-500 hover:text-red-700 disabled:opacity-50"
									disabled={deletingId === address.id}
									onclick={() => handleDelete(address.id)}
								>
									{deletingId === address.id ? '삭제 중...' : '삭제'}
								</button>
							{/if}
						</div>
					</div>

					<div class="space-y-2 text-sm">
						<div class="flex">
							<span class="w-20 text-gray-500">수령인</span>
							<span>{address.recipient}</span>
						</div>
						<div class="flex">
							<span class="w-20 text-gray-500">연락처</span>
							<span>{address.phone}</span>
						</div>
						<div class="flex">
							<span class="w-20 text-gray-500">주소</span>
							<span>
								({address.postal_code}) {address.address}
								{#if address.address_detail}
									{address.address_detail}
								{/if}
							</span>
						</div>
					</div>

					{#if !address.is_default}
						<div class="mt-4 pt-4 border-t">
							<button
								type="button"
								class="px-4 py-2 border border-black rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
								onclick={() => {
									if (confirm('이 배송지를 기본 배송지로 설정하시겠습니까?')) {
										alert('기본 배송지 설정 기능은 준비 중입니다.');
									}
								}}
							>
								기본 배송지로 설정
							</button>
						</div>
					{/if}
				</div>
			{/each}
		</div>

		<div class="mt-6 p-4 bg-gray-50 rounded-lg">
			<p class="text-sm text-gray-600">
				• 최대 10개까지 배송지를 등록할 수 있습니다.<br />
				• 기본 배송지는 삭제할 수 없습니다. 다른 배송지를 기본으로 변경 후 삭제해주세요.
			</p>
		</div>
	{/if}
</div>
