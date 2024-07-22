// components/Header.tsx

import Link from "next/link";

type Props = {
  title: string;
};

export default function Header({ title }: Props) {
  return (
    <header className="bg-[#d8f9fa] px-4 py-3">
      <div className="max-w-screen-xl mx-auto flex justify-between items-center">
        <h1 className="text-2xl">{title}</h1>
        <nav>
          <ul className="list-none m-0 p-0">
            <li>
              <Link href="/">トップページへ戻る</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
