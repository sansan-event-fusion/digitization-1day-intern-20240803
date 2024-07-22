// app/page.tsx
import Header from "./header";
import EntryPanel from "./entryPanel";

export default async function Page() {
  return (
    <div>
      <Header title="入力画面" />
      <EntryPanel />
    </div>
  );
}
