# Project setup guide

## Prerequisites

Before getting started, ensure you have the following installed on your machine:

- [Node.js](https://nodejs.org/) (version 21.x or higher)

## Running the Project

**Install the dependencies:**

```bash
 npm install
```

**start the development server:**

```bash
 npm run dev
```

## Changing the URL in Constants

If you need to change the base URL used in the project, you can do so by editing the constants.js file located in the src/utils directory. Follow these steps:

```bash
export const BASE_URL = 'http://your-backend-url.com';

```

## If you don't have nodejs version 21

If you don't have Node.js version 21.x installed, you can use `nvm` to manage different Node.js versions. Here's how:

1. Install `nvm` by following the instructions on the [nvm GitHub page](https://github.com/coreybutler/nvm-windows).

2. Once `nvm` is installed, you can install the required Node.js version by running the following command :

   ```bash
   nvm install 21
   ```

3. After installing Node.js, you can set it as the default version:

   ```bash
   nvm use 21
   ```

4. Verify that Node.js is installed and the correct version is active:

   ```bash
   node --v
   ```

5. Once you have the correct version of Node.js installed, proceed with installing the project dependencies and running the project as described in the Installation and Running the Project sections.
