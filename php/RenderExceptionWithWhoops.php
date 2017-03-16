<?php 

namespace App\Traits;

/**
 * use this trait in `render` method of your Exceptions/Handler.php,
 * and use below code to render the error using whoops:
 * `return $this->renderExceptionWithWhoops($e);`
 */
trait RenderExceptionWithWhoops {
    private function renderExceptionWithWhoops(\Exception $e)
    {
        $whoops = new \Whoops\Run;
        $whoops->pushHandler(new \Whoops\Handler\PrettyPageHandler);

        return $whoops->handleException($e);
    }
}
