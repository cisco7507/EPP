import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to the EPP GUI</h1>
        <p className="text-lg mb-8">
          Manage your domain registry operations with ease.
        </p>
        <Link href="/profiles" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded text-xl mr-4">
          Go to Registry Profiles
        </Link>
        <Link href="/domains/check" className="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded text-xl">
          Check a Domain
        </Link>
      </div>
    </main>
  );
}
