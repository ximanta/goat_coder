'use client';
import './globals.css';


export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang='en' className='dark'>
      <head>
        <script src='https://cdn.tailwindcss.com'></script>{' '}
      </head>
      <body className='min-h-screen w-full'>
         {children}
      </body>
    </html>
  );
}
