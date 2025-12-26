import { writable } from 'svelte/store';
import type { Session, User } from '@supabase/supabase-js';

interface AuthState {
	user: User | null;
	session: Session | null;
	loading: boolean;
	initialized: boolean;
}

export const authStore = writable<AuthState>({
	user: null,
	session: null,
	loading: true,
	initialized: false
});
