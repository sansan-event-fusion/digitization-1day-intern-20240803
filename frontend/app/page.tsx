import Link from "next/link";

export default async function Page() {
  return (
    <div>
      <div>
        <Link href="/delivery">データ化完了名刺一覧</Link>
      </div>
      <div>
        <Link href="/inspector-entry">入力画面</Link>
      </div>
    </div>
  );
}
