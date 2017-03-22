<?php

namespace App\Traits;

use Illuminate\Http\Request;
use Whoops\Handler\JsonResponseHandler;
use Whoops\Handler\PrettyPageHandler;

trait RenderExceptionWithWhoops
{
    private function renderExceptionWithWhoops(Request $request, \Exception $e)
    {
        $handler = $request->ajax() ? new JsonResponseHandler : new PrettyPageHandler;
        if ($editor = config('whoops.editor')) {
            // https://github.com/filp/whoops/blob/master/docs/Open%20Files%20In%20An%20Editor.md
            $handler->setEditor('sublime');
        }
        
        $whoops = new \Whoops\Run;
        $whoops->pushHandler($handler);
        return new \Illuminate\Http\Response(
            $whoops->handleException($e),
            $e->getStatusCode(),
            $e->getHeaders()
        );
    }
}
