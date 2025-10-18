import AddProfileForm from '@/components/add-profile-form';

export default function NewProfilePage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <div className="w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-4">Add New Registry Profile</h1>
        <AddProfileForm />
      </div>
    </main>
  );
}
