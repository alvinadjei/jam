// import Image from "next/image";

export default function Home() {
  return (
    <div>
      <main className="flex flex-col items-center w-[dw]">
        <div className="flex justify-center">
          <a>
            Logo
          </a>
          <nav className="flex mx-10">
            <ul className="flex mx-10">
              <li>link 1</li>
              <li>link 2</li>
              <li>link 3</li>
            </ul>
          </nav>
        </div>
        Hello, World!
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        Footer
      </footer>
    </div>
  );
}
